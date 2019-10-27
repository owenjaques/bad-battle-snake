import json
from flask import Flask, request
from api import ping_response, start_response, move_response, end_response
from snake import Snake
from model import Model

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def route_root():
	return "This boy is a snake!"

@app.route('/ping', methods = ['GET', 'POST'])
def ping():
	return ping_response()

@app.route('/start', methods = ['GET', 'POST'])
def start():
	print("***START***")
	global snake
	snake = Snake(Model())
	return start_response()

@app.route('/move', methods = ['GET', 'POST'])
def move():
	global snake
	data = request.get_json()
	move = snake.getDirection(data)
	print("turn = ", data['turn'], "moving ", move)
	return move_response(move)

@app.route('/end', methods = ['GET', 'POST'])
def end():
	print("***END***")
	return end_response()

if __name__ == '__main__':
	# port = input("Please enter the port ex:'8080'")
	global snake
	snake = Snake(Model())
	app.run(host='0.0.0.0', port=8080, threaded=False)#had issues with the model predicting with multi threading