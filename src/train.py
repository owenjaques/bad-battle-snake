import numpy as np
import random
from keras import Sequential
from keras.layers import InputLayer, Dense, Flatten, Reshape

#I wanted to use static variables in the functions like c but I couldn't quite get it
s = []
direction = 1

def createModel():
	global model
	model = Sequential()
	model.add(InputLayer(input_shape=(13,13,4), batch_size=1))
	model.add(Dense(32, activation='relu'))
	model.add(Dense(32, activation='relu'))
	model.add(Dense(32, activation='relu'))
	model.add(Flatten())
	model.add(Dense(4, activation='softmax'))
	model.compile(loss='mse', optimizer='adam')
	#loads weights comment out if you want new **WILL DELETE OLD WEIGHTS**
	try:
		model.load_weights('weights.h5')
		print("Loaded weights from weights.h5")
	except Exception as e:
		print(e)

def getReward(data):
	#gives rewards to the snake depending if the last move was a desired behavior
	if data['you']['health'] == 0 or data['turn'] == 0:
		print("Snake died last turn")
		return -10
	elif data['you']['health'] == 100 and data['turn'] != 0:
		print("Snake ate some munch last turn")
		return 1
	else:
		print("Snake stayed alive last turn")
		return 0.5

def getState(data):
	#maps the game board to determine a state
	BOARDWIDTH = 13
	game_board = np.zeros((1, BOARDWIDTH, BOARDWIDTH, 4), dtype=int)
	HEAD = 1
	SNAKEPART = 2
	FOOD = 3

	#adds walls to map
	for i in range(BOARDWIDTH):
		game_board[0][i][0][SNAKEPART] = 1
		game_board[0][i][BOARDWIDTH-1][SNAKEPART] = 1
		game_board[0][0][i][SNAKEPART] = 1
		game_board[0][BOARDWIDTH-1][i][SNAKEPART] = 1

	#adds all snake parts to map
	for snake in data['board']['snakes']:
		for points in snake['body']:
			x = points['x'] + 1
			y = points['y'] + 1
			game_board[0][y][x][SNAKEPART] = 1

	#adds all food to map
	for food in data['board']['food']:
		x = food['x'] + 1
		y = food['y'] + 1
		game_board[0][y][x][FOOD] = 1

	#adds head to map
	head = data['you']['body'][0]
	x = head['x'] + 1
	y = head['y'] + 1
	game_board[0][y][x][SNAKEPART] = 0
	game_board[0][y][x][HEAD] = 1

	return game_board

	

def getDirection(data):
	#my terrible job of implementing q learning
	#heavily borrowed form a tutorial on machinelearning.com to train a game of cartpole (https://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/)
	global s
	global direction
	global model
	old_direction = direction
	lr = 0.9
	y = 0.5
	eps = 0.3 #lower epsilon to move with less randomness
	directions = ['up', 'down', 'left', 'right']
	new_s = getState(data)
	#tries to keep a bit of randomness
	if random.random() < eps:
		pre = model.predict(new_s)[0]
		print(pre)
		direction = np.argmax(pre)
	else:
		direction = random.randint(0,3)
	#will not execute if there is no former move to reward ie: start of training
	if s != []:
		target_vec = model.predict(s)
		target = getReward(data) + lr*(y*(np.max(model.predict(new_s)[0])))
		target_vec[0][old_direction] = target
		model.fit(s, target_vec, epochs=1, verbose=0)
	s = new_s
	model.save_weights('weights.h5')
	return directions[direction]