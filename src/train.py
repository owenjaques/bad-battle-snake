import numpy as np
import random
from keras import Sequential
from keras.layers import InputLayer, Dense, Reshape, Conv2D, MaxPool2D, Flatten

s = []
direction = 1

def createModel():
	global model
	model = Sequential()
	model.add(InputLayer(batch_input_shape=(13,13)))
	model.add(Dense(100, activation='sigmoid'))
	model.add(Dense(4, activation='linear'))
	model.compile(loss='mse', optimizer='adam', metrics=['mae'])
	#loads weights comment out if you want new **WILL DELETE OLD WEIGHTS**
	try:
		model.load_weights('weights.h5')
		print("Loaded weights from weights.h5")
	except Exception as e:
		print(e)

def getReward(data):
	if data['you']['health'] == 0 or data['turn'] == 0:
		return -1
	elif data['you']['health'] == 100 and data['turn'] != 0:
		return 0.5
	else:
		return 1

def getState(data):
	#maps the game board to determine a state
	BOARDWIDTH = 13
	game_board = np.zeros((BOARDWIDTH, BOARDWIDTH), dtype=int)
	HEAD = 1
	SNAKEPART = 2
	FOOD = 3

	#adds walls to map
	for i in range(BOARDWIDTH):
		game_board[i][0] = SNAKEPART
		game_board[i][BOARDWIDTH-1] = SNAKEPART
		game_board[0][i] = SNAKEPART
		game_board[BOARDWIDTH-1][i] = SNAKEPART

	#adds all snake parts to map
	for snake in data['board']['snakes']:
		for points in snake['body']:
			x = points['x'] + 1
			y = points['y'] + 1
			game_board[y][x] = SNAKEPART

	#adds all food to mao
	for food in data['board']['food']:
		x = food['x'] + 1
		y = food['y'] + 1
		game_board[y][x] = FOOD

	#adds head to map
	head = data['you']['body'][0]
	x = head['x'] + 1
	y = head['y'] + 1
	game_board[y][x] = HEAD

	print(game_board)

	return game_board

	

def getDirection(data):
	#my terrible job of implementing q learning slapped in some extra numbers in there to mess with it
	#heavily borrowed form a tutorial on machinelearning.com (https://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/)
	global s
	global direction
	global model
	old_direction = direction
	lr = 0.001
	y = 0.95
	eps = 0.5
	directions = ['up', 'down', 'left', 'right']
	new_s = getState(data)
	#tries to keep a bit of randomness 
	if 0.5*random.random() < eps:
		direction = np.argmax(model.predict(new_s)[0])
		print(model.predict(new_s)[0])
	else:
		direction = random.randint(0,3)
	if s != []:
		target_vec = model.predict(s)
		target = getReward(data) + lr*(y*(np.max(model.predict(new_s)[0])))
		target_vec[0][old_direction] = target
		model.fit(s, target_vec, epochs=1, verbose=0)
	s = new_s
	model.save_weights('weights.h5')
	return directions[direction]