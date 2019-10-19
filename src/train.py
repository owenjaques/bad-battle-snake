import numpy as np
import random

q_table = {}

directions = ['up', 'down', 'left', 'right']

# def getReward(data):
# 	if data['you']['health'] == 0:
# 		do bad thing
# 	elif data['you']['health'] == 100:
# 		do good thing
# 	else
# 		do ok thing

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

	#turns gameboard array into unique string
	# b_id = ""
	# for i in range(BOARDWIDTH):
	# 	for j in range(BOARDWIDTH):
	# 		b_id += str(game_board[i][j])

	# return b_id

	return game_board

	

def getDirection(data):
	directions = ['up', 'down', 'left', 'right']
	s = getState(data)
	direction = random.randint(0,3)
	# if s in q_table:
	# 	direction = np.amax(q_table[s])
	# else:
	# 	q_table[s] = np.zeros((5))

	# print(q_table)

	return directions[direction]