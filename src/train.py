import numpy as np
import random
from keras import Sequential
from keras.layers import InputLayer, Dense, Flatten

q_table = {}
s = []
direction = 1

def createModel():
	global model
	model = Sequential()
	model.add(InputLayer(batch_input_shape=(11,11)))
	model.add(Dense(64, activation='sigmoid'))
	model.add(Dense(4, activation='linear'))
	model.compile(loss='mse', optimizer='adam', metrics=['mae'])
	try:
		model.load_weights('model.h5')
		print("Loaded weights from model.h5")
	except Exception as e:
		print(e)

def getReward(data):
	if data['you']['health'] == 0 or data['turn'] == 0:
		return -20
	elif data['you']['health'] == 100:
		return 10
	else:
		return 20

def getState(data):
	#maps the game board to determine a state
	BOARDWIDTH = 11
	game_board = np.zeros((BOARDWIDTH, BOARDWIDTH), dtype=int)
	HEAD = 1
	SNAKEPART = 2
	FOOD = 3

	#adds all snake parts to map
	for snake in data['board']['snakes']:
		for points in snake['body']:
			x = points['x']
			y = points['y']
			game_board[y][x] = SNAKEPART

	#adds all food to mao
	for food in data['board']['food']:
		x = food['x']
		y = food['y']
		game_board[y][x] = FOOD

	#adds head to map
	head = data['you']['body'][0]
	x = head['x']
	y = head['y']
	game_board[y][x] = HEAD

	#creates unique string to represent state
	# id = ""
	# for i in range(11):
	# 	for j in range(11):
	# 		id += str(game_board[i][j])

	return game_board

	

def getDirection(data):
	#my terrible job of implementing q learning slapped in some extra numbers in there to mess with it
	#heavily borrowed form a tutorial on machinelearning.com (https://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/)
	global s
	global direction
	global model
	old_direction = direction
	lr = 0.8
	y = 0.95
	eps = 0.5
	directions = ['up', 'down', 'left', 'right']
	new_s = getState(data)
	#tries to keep a bit of randomness 
	if 0.5*random.random() < eps:
		direction = np.argmax(model.predict(new_s)[0])
	else:
		direction = random.randint(0,3)
	if s != []:
		target = getReward(data) + lr*(y*np.max(model.predict(new_s)[0]))
		target_vec = model.predict(s)
		target_vec[0][old_direction] = target
		model.fit(s, target_vec, epochs=1, verbose=0)
	s = new_s
	model.save_weights('model.h5')
	return directions[direction]