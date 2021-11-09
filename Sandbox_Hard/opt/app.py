"""
Very simple Flask App.  For Testing
"""

import sys

import flask
from flask_socketio import SocketIO

import logging
log = logging.getLogger("APP")

import handler

app = flask.Flask(__name__)
socketio = SocketIO(app)

RED="\u001b[31m"
YELLOW="\u001b[33m"
RESET="\u001b[0m"
BOLD="\u001b[1m"
WHITE="\u001b[37m"

def theFilter(theText):
    """
    Whatever filtering needs to take place
    """

    #No filter this time around
    denylist = ["socket"]
    for item in denylist:
        if item in theText.lower():
            #socketio.send()
            return True, f"{YELLOW}{BOLD}Illegal Command Detected: {RED}{item}{RESET}"
    
    return False, theText

def execute(theCommand):
    """ 
    Run a Command, in the sandbox
    """

    #Mangle the command so we get some output
    theCommand = "out = {0}".format(theCommand)
    
    #Destroy the locals
    globs = {"__builtins__": None}
    #Output of the command is stored in the locals, so lets return that
    locs = {}
    try:
        exec(theCommand, globs, locs)
    except Exception as ex:
        log.warning(ex)
        return "{0}{1}{2}{3}".format(RED, BOLD, ex, RESET)

    return "Command Success"

@app.route('/', methods=["GET","POST","OPTIONS"])
def main():
    """Oh no you don't
    """
    return handler.handleRequest(flask.request)
    
@app.after_request
def addHeaders(resp):
    resp.headers["allow"] = "OPTIONS, GET, POST, HEAD"
    return resp

@socketio.on("connect")
def connect():
    version = sys.version
    socketio.send("{1}Python {0}{2}\n1337 Mode Activated".format(version,
                                                                 WHITE,
                                                                 RESET))


@socketio.on('message')
def handle_message(message):

    tripFilter, filtered = theFilter(message)
    if tripFilter:
        socketio.send(filtered)
    else:
        out = execute(filtered)

        if type(out) == bytes:
            socketio.send(out.decode())
        else:
            socketio.send(out)        

@app.route('/debug')
def debug():
    return flask.Response(open(__file__).read(), mimetype='text/plain')
    
if __name__ == "__main__":
    socketio.run(app)
