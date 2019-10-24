import gym
import gym_snake
import random
import time
from collections import deque
from snake import Snake

#Utilizes the gym-snake environment to train locally with some slight modifications
# 1 Remove the check in to see if there are more snakes then there should be in the controller 


def createGame():
	global env
	global NUMSNAKES
	env = gym.make('snake-plural-v0')
	env.grid_size = [11,11]
	env.n_snakes = NUMSNAKES
	env.snake_size = 3
	env.unit_size = 1
	env.unit_gap = 0
	env.num_foods = random.randint(5,10)
	env.random_init = True
	env.reset()
	#set all healths
	for i in range(NUMSNAKES):
		env.controller.snakes[i].health = 100

def getState(obs, snake, turn):
	#creates a dictionary of the game state near identical to the json given by the server
	#makes things much faster
	dic = {
		"turn": turn,
		"board": {
			"snakes": [],
			"food": []
		},
		"you":
			{
				"health": snake.health,
				"body": [{"x": snake.head[0], "y": snake.head[1]}]
			},
	}
	#finds food
	for y in range(11):
		for x in range(11):
			if obs[0][y][x][2] == 255 and obs[0][y][x][1] == 0 and obs[0][y][x][0] == 0:
				dic['board']['food'].append({"x": x, "y": y})

	for i in range(len(env.controller.snakes)):
		#sees if there is a dead snake
		if env.controller.snakes[i] == None:
			break
		x = env.controller.snakes[i].head[0]
		y = env.controller.snakes[i].head[1]
		dic['board']['snakes'].append({"body": []})
		dic['board']['snakes'][i]['body'].append({"x": x, "y": y})
		body = env.controller.snakes[i].body
		for j in range(len(body)):
			x = env.controller.snakes[i].body[j][0]
			y = env.controller.snakes[i].body[j][1]
			dic['board']['snakes'][i]['body'].append({"x": x, "y": y})

	return dic

def filterActions(a):
	if a == 'up':
		return 0
	if a == 'right':
		return 1
	if a == 'down':
		return 2
	if a == 'left':
		return 3

#creates the snakes
my_snakes = []
NUMSNAKES = 2
for _ in range(NUMSNAKES):
	my_snakes.append(Snake())

#used for calculating average
turns = 0

#play a set amount of games (TRIALS)
TRIALS = 10
for trial in range(TRIALS):
	print("TRIAL #", trial)
	createGame()

	#first action for each snake
	actions = []
	for _ in range(NUMSNAKES):
		actions.append(2)

	#maxes out at 250 turns
	for turn in range(250):
		obs = env.step(actions)
		#sees if it needs to quit the loop
		#TODO: see if there is only one snake remaining if so declare snake the winner and end game
		if obs[2] == True:
			print("ended with", turn, "turns")
			break
		turns += 1
		i = 0
		for snake in env.controller.snakes:
			#sees if snake is dead
			if snake == None:
				break
			if obs[1][i] == 1:
				snake.health = 100
			#kills snake if health too low
			elif snake.health <= 0:
				snake = None
				break
			actions[i] = filterActions(my_snakes[i].getDirection(getState(obs, snake, turn,), False, False))
			snake.health -= 1
			#comment out this next line if you don't want to watch
			#env.render(close=True)
			i += 1

#saves model only once for enhanced speed
for snake in my_snakes:
	snake.saveModel()

print("Average turn length:", turns/TRIALS)