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

RED="\u001b[31m"
YELLOW="\u001b[33m"
RESET="\u001b[0m"
BOLD="\u001b[1m"

def theFilter(theText):
    """
    Whatever filtering needs to take place
    """

    #No filter this time around
    denylist = ["socket", "os" ,"popen", "subprocess", "+", "join", "open","'glob'"]
    for item in denylist:
        if item in theText.lower():
            socketio.send(f"{YELLOW}{BOLD}Illegal Command Detected: {RED}{item}{RESET}")
            return False
    
    return theText


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
        filtered = theFilter(message)
        if not filtered:
            return False
        
        out = eval(filtered)
        if type(out) == bytes:
            socketio.send(out.decode())
        else:
            socketio.send(out)
    except Exception as ex:
        socketio.send("{}".format(ex))

@app.route('/debug')
def debug():
   return flask.Response("Not this Time :(")

        
if __name__ == "__main__":
    socketio.run(app)
