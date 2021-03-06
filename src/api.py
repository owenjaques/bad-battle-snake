from flask import Response
import json

def ping_response():
    return Response(
        status=200
    )

def start_response():
    return Response(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        response = json.dumps({
            "color": "#0066ff",
            "body": "smile",
            "tail": "sharp"
        })
    )

def move_response(move):
    assert move in ['up', 'down', 'left', 'right'], \
        "Move must be one of [up, down, left, right]"

    return Response(
		status=200,
        headers={
            "Content-Type": "application/json"
        },
        response = json.dumps({
            "move": move
        })
    )

def end_response():
    return "End Game"