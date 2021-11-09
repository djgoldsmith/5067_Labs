import flask
from flask import session
import re
import logging

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = "FooBar"

def processInput(theText):
    """
    Filter and Process.

    Throw an Error if we detect possible SSTI
    """

    badChars = ["'",'"',"format","socket"]
    regex = re.compile('|'.join(map(re.escape, badChars)))

    matches = regex.findall(theText)
    if matches:
        return "Input Matches {0}".format(matches)

    #Check the Length
    if len(theText) > 150:
        return "Too Long"

    templateStr = "<div class='alert'>{0}</div>".format(theText)
    out = flask.render_template_string(templateStr)
    #Actually lets keep it blind
    return theText
    

@app.route("/login", methods=["GET","POST"])
def login():
    if "user" in session:
        if session["user"] in ["Balthazar", "Melichor", "Gaspar"]:
            #We have logged in correctly, go back to the index
            return flask.redirect(flask.url_for('/'))
            pass

    if flask.request.method == "POST":
        logging.warning(flask.request.form)
        #Otherwise deal with whatever content gets posted
        email = flask.request.form.get("email")
        message = "<div class='alert alert-info'>{0} Not in database</div>".format(email)
        return flask.render_template("login.html", message=message)
        
    return flask.render_template("login.html")

    
@app.route('/', methods=["GET","POST"])
def main():
    
    # if "user" not in session:
    #     session["user"] = "unknown"

    # if session["user"] not in ["Balthazar", "Melichor", "Gaspar"]:
    #     return flask.redirect(flask.url_for('login'))
        
    #flask.session.update(test=1)
    if flask.request.method == "POST":
        theKing = flask.request.form.get('king')
        name = flask.request.form.get('name')
        gift = flask.request.form.get('gift')

        #And Clean the input for each of them
        cleanKing = processInput(theKing)
        cleanName = processInput(name)

        #Gifts we just turn into a list
        cleanGifts = gift.split("\n")

        return flask.render_template("index.html", message={"name":cleanName,
                                                            "king":cleanKing,
                                                            "gifts":cleanGifts})
    #print(out)
    return flask.render_template("index.html")

@app.route('/debug')
def debug():
    return flask.Response(open(__file__).read(), mimetype='text/plain')
