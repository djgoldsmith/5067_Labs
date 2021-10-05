"""
Very simple Flask App.  For Testing
"""


import json
import re

import flask

from .meta import app
#from .objects import *
from .models import *
from .objects import *

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

import logging

            
@app.route("/")
def index():

    logging.warning("Initial Population")

    bookQry = Item.query.filter_by(hidden = False)
    if bookQry.count() == 0:
        logging.warning("Need some Books")
        populateBookTable()

    userQry = User.query.count()
    logging.warning("User Count %d", userQry)
    if userQry == 0:
        logging.warning("Need some Users")
        populateUserTable()

        
    return flask.render_template("index.html",
                                 bookList = bookQry)


@app.route("/about")
def about():
    return flask.render_template("about.html")



@app.route("/secrets")
@app.route("/admin")
@app.route("/phpmyadmin")
@app.route("/backups")
@app.route("/secrets/system_administration")
def dirForbidden():
    """
    Return a Forbidden Page
    """
    flask.abort(403)


@app.route("/.gitignore")
def gitIgnore():
    robots = """
*~
*#
*.bak
*.sql
"""
    response = flask.make_response(robots, 200)
    response.mimetype = "text/plain"
    return response


@app.route("/backups/db.sql")
def returnDB():
    robots = """
FLAG{ENUM_BACKUP_FILES}
"""
    response = flask.make_response(robots, 200)
    response.mimetype = "text/plain"
    return response
    

@app.route("/secrets/system_administration/flag")
def dirbuster():
    """
    Show the flag file
    """
    return flask.render_template("reconflag.html")

@app.route("/accountsettings")
def parametersSearch():

    flag = None
    params = flask.request.args.get("remind_password", None)
    logging.warning("PARAMETERS ARE")
    logging.warning(params)
    if params:
        logging.warning("IS CORRECT")
        flag = "CUEH{PARAMETER_BUSTING}"

    return flask.render_template("parameters.html",
                                 flag = flag)
    
    
@app.route("/login", methods=["GET", "POST"])
def login():

    prev = flask.request.args.get("prev")
    if not prev:
        prev == "index"
        
    if flask.request.method == "POST":
        #Get data
        user = flask.request.form.get("email")
        password = flask.request.form.get("password")

        userQry = User.query.filter_by(email = user).first()
        if userQry is None:
            flask.flash("No Such User")
        else:
            if userQry.password == password:
                flask.session["user"] = userQry.id
                flask.session["role"] = userQry.level
                flask.flash("Login Successful")
                return (flask.redirect(flask.url_for(prev)))

            else:
                flask.flash("Incorrect password for {0}".format(user))
                
        
    return flask.render_template("login.html",
                                 prev = prev)

@app.route("/logout")
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for("index"))


@app.route("/user/create", methods=["GET","POST"])
def create():
    """ Create a new account,
    we will redirect to a homepage here
    """

    if flask.request.method == "GET":
        return flask.render_template("create_account.html")
    
    #Get the form data
    name = flask.request.form.get("name")
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")
    password2 = flask.request.form.get("password2")

    if password != password2:
        flask.flash("Passwords do not match")
        return flask.render_template("create_account.html",
                                     name = name,
                                     email = email)

    logging.warning("Name >%s< %s", name, name == None)
    #Sanity check do we have a name, email and password
    if not name or not email or not password: 
        flask.flash("Not all info supplied")
        return flask.render_template("create_account.html",
                                     name = name,
                                     email = email)
    #And check we have an email
    emailre = re.compile(r"^[\w\.\+\-]+\@[\w]+\.([a-z]{2,3})+$")

    if not emailre.match(email):
        flask.flash("Bad Email Address")
        return flask.render_template("create_account.html",
                                     name = name)

    #Otherwise we can add the user
    userQry = User.query.filter_by(email = email).first()
    if userQry:
        flask.flash("A User with that Email Exists")
        return flask.render_template("create_account.html",
                                     name = name,
                                     email = email)

    else:
        #Crate the user
        theUser = User(name=name,
                       email=email,
                       password=password)

        db.session.add(theUser)
        db.session.commit()
        flask.flash("Account Created, you can now Login")
        return flask.redirect(flask.url_for("login"))


    
@app.route("/user/<userId>/settings")
def settings(userId):

    #Yes its silly that I forgot cookies, let pretend its an API
    thisUser = User.query.filter_by(id=userId).first()
    if not thisUser:
        flask.flash("No Such User")
        return flask.redirect(flask.url_for("index"))
    
    return flask.render_template("usersettings.html",
                                 user = thisUser)

@app.route("/user/<userId>/update", methods=["GET","POST"])
def updateUser(userId):

    thisUser = User.query.filter_by(id = userId).first()
    if not thisUser:
        flask.flash("No Such User")
        return flask.redirect(flask_url_for("index"))

    #otherwise we want to do the checks
    if flask.request.method == "POST":
        logging.warning("------------------------")
        current = flask.request.form.get("current")
        password = flask.request.form.get("password")
        if current:
            if current == thisUser.password:
                thisUser.password = password
                db.session.commit()
            else:
                flask.flash("Current Password is incorrect")
            return flask.redirect(flask.url_for("settings",
                                                userId = thisUser.id))

        adminSubmit = flask.request.form.get("updateadmin")
        logging.warning("Admin Submit %s", adminSubmit)
        if adminSubmit:
            admin = flask.request.form.get("admin")
            logging.warning("Admin Box is %s", admin)
        
            if admin:
                admin = "admin"
            else:
                admin = "user"

            thisUser.level = admin
            #And update the Session
            flask.session["role"] = admin
            db.session.commit()
            logging.warning(" UPDATING THE ADMIN ")
            logging.warning("Level %s ", thisUser.level)
            return flask.redirect(flask.url_for("settings", userId=userId))
            
    #if thisUser.id != flask.session["user"]
    #And then update the settings
    #if
    flask.flash("Update Error")

    return flask.redirect(flask.url_for("settings", userId=userId))
    


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return flask.render_template('404.html', e = e), 404


# @app.route('/')
# def main():
#     #payload = flask.request.args.get("payload")
#     return flask.render_template('index.html')


# @app.route("/admin")
# def admin():
#     return flask.render_template('admin.html')


# @app.route("/my")
# @app.route("/my/admin/")

# def enum():
#     return flask.render_template('enum.html')


# @app.route("/my-sql")
# def badEnum():
#     flask.abort(403)
#     return "foo"

# @app.route("/my-sql/admin")
# @app.route("/my/admin/spider")
# def enumSuccess():

#     #Can i get the route
# #    flask.request.route
    
#     return flask.render_template('enum.html',
#                                  success=True)
    
