import numpy as np
import random

q_table = {}
s = ""
direction = 1

def getReward(data):
	if data['you']['health'] == 0 or data['turn'] == 0:
		return -5
	elif data['you']['health'] == 100:
		return 1
	else:
		return 0.5

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
	id = ""
	for i in range(11):
		for j in range(11):
			id += str(game_board[i][j])

	return id

	

def getDirection(data):
	#my terrible job of implementing q learning slapped in some extra numbers in there to mess with it
	#heavily borrowed form a tutorial on machinelearning.com (https://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/)
	global s
	global direction
	old_direction = direction
	lr = 0.8
	y = 0.95
	directions = ['up', 'down', 'left', 'right']
	new_s = getState(data)
	if new_s not in q_table:
		direction = random.randint(0,3)
		q_table[new_s] = np.zeros(4)
	#tries to keep a bit of randomness 
	else:
		if random.random() < np.max(q_table[s]):
			direction = np.argmax(q_table[s])
		else:
			direction = random.randint(0,3)
	if s != "":
		q_table[s][old_direction] += 0.8*getReward(data) + 0.2*lr*(y*np.max(q_table[new_s]))
	s = new_s


	print(q_table)
	

	return directions[direction]