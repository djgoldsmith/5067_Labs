"""
Demoing Cookies
"""

import json
import logging

import flask
from .meta import app
from .meta import auth


@auth.verify_password
def verifyPassword(username, password):
    logging.warning("--- PASSWORD VERIFICATION REQUESTED ----")
    if username == "Erebus":
        if password == "Davin":
            return True
        
    return False


@app.route("/sessions/basicAuth")
@auth.login_required
def basicAuth_Demo():
    return flask.render_template("basicAuth_demo.html")


@app.route('/sessions/basiclogout')
def basiclogout():    
    return ('Logout', 401)



@app.route("/sessions/storingState", methods=["GET","POST"])
def formState():

    username = flask.request.form.get("user")
    isAdmin = flask.request.form.get("admin",None)
    
    return flask.render_template("formState.html",
                                 uName = username,
                                 admin = isAdmin
                                 )


@app.route("/sessions/cookiesState", methods=["GET","POST"])
def cookieDemo():

    username = flask.request.form.get("user")
    if not username:
        username = flask.request.cookies.get("user")
    isAdmin = flask.request.cookies.get("admin","False")
    attempts = flask.request.cookies.get("attempts",0)

    attempts = int(attempts)
    
    theTemplate = flask.render_template("cookieDemo.html",
                                        uName = username,
                                        admin = isAdmin,
                                        attempts = attempts                                        
                                        )
    resp = flask.Response(theTemplate)
    if username:
        resp.set_cookie('user', username, max_age=60*5, samesite="Strict")
        resp.set_cookie('admin', isAdmin, max_age=60*5, samesite="Strict")
    attempts+= 1
    resp.set_cookie('attempts', str(attempts), max_age=60*5, samesite="Strict")


    return resp



@app.route("/sessions/sessionState", methods=["GET","POST"])
def sessionDemo():    
    username = flask.request.form.get("user")
    if not username:
        username = flask.session.get("user")
    isAdmin = flask.session.get("admin","False")
    attempts = flask.session.get("attempts",0)

    attempts = int(attempts)

    if username:
        flask.session['user'] = username
        flask.session['admin'] = isAdmin
    flask.session['attempts'] = str(attempts)
        
    return flask.render_template("sessionDemo.html",
                                 uName = username,
                                 admin = isAdmin,
                                 attempts = attempts                                        
                                 )



@app.route("/challenges/sessionChallenge", methods=["GET","POST"])
def sessionChallenge():    
    username = flask.request.form.get("user")
    if not username:
        username = flask.session.get("user")
    isAdmin = flask.session.get("admin","False")
    attempts = flask.session.get("attempts",0)

    attempts = int(attempts)

    
    
    if username:
        flask.session['user'] = username
        flask.session['admin'] = isAdmin
    flask.session['attempts'] = str(attempts)
        
    return flask.render_template("sessionChallenge.html",
                                 uName = username,
                                 admin = isAdmin,
                                 attempts = attempts,
                                 secretKey = app.secret_key
                                 )



@app.route("/challenges/cookieChallenge", methods=["GET","POST"])
def cookieChallenge():

    username = flask.request.form.get("user")
    if not username:
        username = flask.request.cookies.get("user")
    isAdmin = flask.request.cookies.get("adminChallenge","False")
    
    theTemplate = flask.render_template("cookieChallenge.html",
                                        uName = username,
                                        admin = isAdmin,
                                        )
    resp = flask.Response(theTemplate)
    if username:
        resp.set_cookie('user', username, max_age=60*5, samesite="Strict")
        resp.set_cookie('adminChallenge', isAdmin, max_age=1, samesite="Strict")

    return resp


@app.route("/challenges/cookieCheck")
def cookieCheck():

    import time
    time.sleep(1)
    isAdmin = flask.request.cookies.get("adminChallenge","False")

    return flask.render_template("cookieCheck.html",
                                 admin = isAdmin)






