import json
from flask import Flask, request
from api import ping_response, start_response, move_response, end_response

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
    return start_response()

@app.route('/move', methods = ['GET', 'POST'])
def move():
    data = request.get_json()
    direction = 'up'
    return move_response(direction)

@app.route('/end', methods = ['GET', 'POST'])
def end():
    print("***END***")
    return end_response()

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)