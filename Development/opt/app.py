"""
Very simple Flask App.  For Testing
"""

import sys

import flask
from flask_socketio import SocketIO

import logging
log = logging.getLogger("APP")


app = flask.Flask(__name__)
socketio = SocketIO(app)


@app.route('/', methods=["GET","POST"])
def main():
    return flask.render_template('index.html')

@socketio.on("connect")
def connect():
    version = sys.version
    socketio.send("Python {0}".format(version))

@socketio.on('message')
def handle_message(message):
    try:
        out = eval(message)
        if type(out) == bytes:
            socketio.send(out.decode())
        else:
            socketio.send(out)
    except Exception as ex:
        socketio.send("{}".format(ex))

@app.route('/debug')
def debug():
   return flask.Response(open(__file__).read(), mimetype='text/plain')

        
if __name__ == "__main__":
    socketio.run(app)
