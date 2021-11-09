"""
Very simple Flask App.  For Testing
"""

import flask
import helper.processGifts as processGifts
import logging
app = flask.Flask(__name__)

errorPage = """
{% extends 'base.html' %}
{% block content %}
<h2>Error</h2>
<div class="alert alert-danger" role="alert">
ERROR:  WHO is not a King
</div>
{% endblock content %}
"""

def showError(theKing = None):
    """
    Display an Error Message to the users
    """
    if not theKing:
        theKing = "Unknown King"
    return flask.render_template_string(errorPage.replace("WHO", theKing))


@app.route('/', methods=["GET","POST"])
def main():
    
    message = {} #Stuff to Return 

    #Do we have a form submission
    if flask.request.method == "POST":
        
        theKing = flask.request.form.get('king')
        if theKing not in ["Balthazar", "Melichor", "Gaspar"]:
            return showError(theKing)

        message["king"] = theKing
        message["name"] = flask.request.form.get('name')
        gift = flask.request.form.get('gift')
        message["gifts"] = processGifts.boloRei(gift)
        
    return flask.render_template('index.html', message=message)

@app.route('/debug')
def debug():
    return flask.Response(open(__file__).read(), mimetype='text/plain')

@app.route('/robots.txt')
def robots():
    robots = """
User-Agent: *
Disallow: /debug
"""
    response = flask.make_response(robots, 200)
    response.mimetype = "text/plain"
    return response

