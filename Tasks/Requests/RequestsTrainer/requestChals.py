"""
Request Based Challenges
"""

import json

import flask
from .meta import app

import logging

import time
import random
import string
import hashlib

#Store the data
automateData = {"time":None,
                "q1": None,
                "q2": None}

@app.route("/challenges/setUA", methods=["GET","POST"])
def userAgentChallenge():

    UA = flask.request.headers.get("User-Agent")

    theFlag = False

    if UA == "Googlebot/2.1":
        theFlag = "5067{Ch@nging_UA}"
    
    return flask.render_template("userAgentChal.html",
                                 flag = theFlag)


def checkFormChal(user, date, secret):
    """ Check if the form challenge fails """

    errors = []
    if user != "azreal":
        errors.append("Incorrect User. {0} != azreal".format(user))
    if date != "-1":
        errors.append("Incorrect Date. {0} != -1".format(date))
    if secret != "luther":
        errors.append("Incorrect Secret. {0} != luther".format(secret))

    
    return errors
                    

@app.route("/challenges/formData", methods=["GET","POST"])
def formDataChallenge():

    theFlag = None
    fails = []
    
    if flask.request.args.get("user"):
        logging.warning("User sent")
        user = flask.request.args.get("user")
        date = flask.request.args.get("date")
        secret = flask.request.args.get("secret")

        fails = checkFormChal(user, date, secret)
        if len(fails) == 0:
            theFlag = "5067{MangleFormD4ta}"
            
    elif flask.request.form.get("user"):
        user = flask.request.form.get("user")
        date = flask.request.form.get("date")
        secret = flask.request.form.get("secret")

        fails = checkFormChal(user, date, secret)
        if len(fails) == 0:
            theFlag = "5067{Th3_Secr3ts_Out}"

    
    return flask.render_template("formDataChal.html",
                                 feedback=fails,
                                 flag = theFlag)


def _jsonAPIResp(feedback, flag):
    output = {"feedback": feedback,
              "flag": flag}
    
    response = app.response_class(
        response=json.dumps(output),
        status=200,
        mimetype='application/json'
    )
    #What we want is the same information
    return response

@app.route("/challenges/APIData", methods=["GET","POST"])
def apiDataChallenge():

    feedback = ["Incorrect Request"]
    theFlag = None

    user = None
    role = None
    
    logging.warning("------------ API CHAL -------------")
    logging.warning(" - METHOD:  {0}".format(flask.request.method))
    if flask.request.method == "POST":
        feedback = ["Correct Request Method"]
        
        user = flask.request.form.get("user")
        role = flask.request.form.get("role")
        
    if flask.request.json:
        logging.warning("--- JSON ---")
        logging.warning(flask.request.json)
        user = flask.request.json.get("user")
        role = flask.request.json.get("role")

    if user == "abbadon" and role == "despoiler":
        theFlag = "5067{FailBaddon_The_Armless}"    
    else:
        feedback.append("Incorrect Request Data")

            
    #And make the ouput JSON if we are feling nice
    if "application/json" in flask.request.headers["accept"]:
        logging.warning("JSON Accept")
        return _jsonAPIResp(feedback, theFlag)

    if flask.request.content_type:
        if flask.request.content_type.startswith("application/json"):
            logging.warning("JSON CONTENT TYPE")
            return _jsonAPIResp(feedback, theFlag)
            return "JSON"

            
    return flask.render_template("apiDataChal.html",
                                 feedback = feedback,
                                 flag = theFlag)

@app.route("/challenges/Response")
def responseChallenge():
    return flask.render_template("responseTarget.html"), 302

@app.route("/challenge/theResponse")
def responsePage():
    return flask.render_template("responseChallenge.html")


@app.route("/challenge/automate", methods=["GET","POST"])
def automateSimple():

    feedback = None
    
    if flask.request.method == "POST":
        #Parse the data
        current = time.time()
        old = flask.session.get("simpletime")
        logging.warning("---- AUTOMATE ----")

        userhash = flask.request.form.get("answer")
        targetHash = flask.session.get("simplehash")
        logging.warning("My Hash %s", targetHash)
        logging.warning("User hash %s", userhash)
        randomString = flask.session["magicword"]
        theFlag = None
        
        #Now we do the comparison
        if userhash == targetHash:
            logging.warning("==> Hash is correct")

            #Now check the time diff
            tDiff = current - old
            logging.warning("Curr %s Old %s Diff %s", current, old, tDiff)
            if tDiff > 5:
                feedback = "Too Slow you took {0} seconds".format(tDiff)
                randomString = "".join(random.choices(string.ascii_letters, k=20))
                flask.session["simpletime"] = time.time()
                flask.session["simplehash"] = hashlib.md5(randomString.encode()).hexdigest()
                flask.session["magicword"] = randomString

            else:
                feedback = "Hash Is correct"
                theFlag = "5067{AutoM8_Requ3sts}"
        else:
            feedback = "Incorrect Input"
        
    else:
        randomString = "".join(random.choices(string.ascii_letters, k=20))
        flask.session["simpletime"] = time.time()
        flask.session["simplehash"] = hashlib.md5(randomString.encode()).hexdigest()
        flask.session["magicword"] = randomString
    
    return flask.render_template("automateHash.html",
                                 magicword = randomString,
                                 feedback = feedback,
                                 theFlag = theFlag)



@app.route("/challenge/automateStart")
def automateStart():

    theToken = "".join(random.choices(string.ascii_letters, k=20))
    flask.session["csrf"] = theToken
    flask.session["csrf-time"] = time.time()
    
    #We want to generate a CSRF token for the form
    return flask.render_template("automateStart.html",
                                 csrf = theToken)
    

@app.route("/challenge/automateUser", methods=["GET", "POST"])
def automateChallenge():

    submitted = False
    flag = False


    #What we now want to do is check the CSRF token
    if flask.request.method == "GET":
        flask.abort(403, "Wrong Request Type")    

    
    if flask.request.method == "POST":
        logging.warning("===== Automate Challenge Started =====")
        #Compare to the CSRF token

        submittedToken = flask.request.form.get("csrf")
        sessToken = flask.session.get("csrf")

        logging.warning("Token %s  Submitted %s", submittedToken, sessToken)
        if submittedToken != sessToken:
            #We have a failiure
            flask.abort(403, "CSRF Token Mismatch")

        #And check the time
        csrfTime = flask.session.get("csrf-time", 0)
        now = time.time()

        tDiff = now - csrfTime
        logging.warning("T1 %d T2 %d Diff %d", csrfTime, now, tDiff)
        #if tDiff > 60:
        #    flask.abort(403, "CSRF Token Expired")
    
        #Check if the answers submitted are correct
        answer1 =  flask.request.form.get("q1")
        answer2 =  flask.request.form.get("q2")
        if answer2 is not None:
            answer2 = hashlib.md5(answer2.encode()).hexdigest()

        
        correct1 = flask.session.get("q1")
        correct2 = flask.session.get("q2")
        
        logging.warning("A1 %s A2 %s", answer1, answer2)
        logging.warning("C1 %s C2 %s", correct1, correct2)
        
        if answer1 is not None:
            logging.warning("--- Answer 1 Sumbitted --")
            logging.warning("%s == %s %s", answer1, correct1, answer1==correct1)

            logging.warning("%s == %s %s", answer2, correct2, answer2==correct2)

            if (answer1 == correct1) and (answer2 == correct2):
                submitted = True
                flag = "CUEH{TEMP}"
            else:
                submitted = "Incorrect"

    #Otherwise we ask our question
    p1 = random.randrange(10)
    p2 = random.randrange(10)
    q1 = "{0} + {1}".format(p1, p2)
    q1a = p1 + p2

    q2 = random.choice(["Lion El'Jonson",
                        "Fulgrim",
                        "Perturabo",
                        "Jaghatai Khan",
                        "Leman Russ",
                        "Rogal Dorn",
                        "Konrad Curze",
                        "Sanguinius", 
                        "Ferrus Manus",
                        "Angron",
                        "Roboute Guilliman",
                        "Mortarion",
                        "Magnus the Red",
                        "Horus",
                        "Lorgar",
                        "Vulkan",
                        "Corax",
                        "Alpharius Omegon"])

    
    #Generate a new CSRF Token
    csrfToken = "".join(random.choices(string.ascii_letters, k=20))
    flask.session["csrf"] = csrfToken
    logging.warning("-- NEW CSRF %s == %s", csrfToken, flask.session["csrf"])

    #And Store our Answers
    flask.session["q1"] = str(q1a)
    flask.session["q2"] = hashlib.md5(q2.encode()).hexdigest()
    
    
    return flask.render_template("automateChallenge.html",
                                 q1 = q1,
                                 q2 = q2,
                                 submitted = submitted,
                                 flag = flag,
                                 csrf = csrfToken)

