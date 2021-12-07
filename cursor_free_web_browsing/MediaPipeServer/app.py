from os import name
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', logger=True)


@socketio.on('connect', namespace='/extension')
def connect_extension():
    print('Extension connected')


@socketio.on('disconnect', namespace='/extension')
def disconnect_extension():
    print('Extension disconnected')


@socketio.on('connect', namespace='/mediapipe')
def connect_mediapipe():
    print('Mediapipe connected')


@socketio.on('disconnect', namespace='/mediapipe')
def disconnect_mediapipe():
    print('Mediapipe connected')


@socketio.on('message', namespace='/mediapipe')
def message_mediapipe(message):
    print(f'Mediapipe send {message} to extension')
    socketio.send(message, namespace='/extension')


if __name__ == '__main__':
    socketio.run(app, debug=True)
