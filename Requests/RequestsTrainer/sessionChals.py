## Challenge For Basic Auth

import logging
import base64

import flask


from .meta import app
from .meta import bauth

@bauth.verify_token
def verify_token(token):
    if token == "EJUBeTGBlI":
        return True

@app.route("/sessions/challenges/basicAuth")
def basicAuth_Challenge():

    msg = None
    
    logging.warning(flask.request.headers)
    authToken = flask.request.headers.get("Authorization")
    logging.warning("Auth Token %s", authToken)

    #Work out the Hash
    hashStr = b"Lorgar:Cadia"

    if authToken:
        b64Str = base64.b64encode(hashStr)
        logging.warning("Encoded\t\t %s", b64Str)

        if not "Basic" in authToken:
            msg = "Incorrect Basic Auth Format"
        else:
            authStr = authToken.strip("Basic").strip().encode()
            logging.warning("Auth str\t>%s<", authStr)
            if authStr == b64Str:
                logging.warning("Correct Creds")
                msg = "Have a Flag 5067{B@s1c_Enc0d3}"
            else:
                logging.warning("IncoorectCreds")
                msg = "Incorrect Username or Password"
            
    return flask.render_template("basicAuth_challenge.html",
                                 msg = msg)


@app.route("/sessions/challenges/tokenAuth")
@bauth.login_required
def tokenAuth_Challenge():
    flag = "5067{Token_Acc3pted}"
    return flask.render_template("tokenAuth_challenge.html",
                                 flag=flag)



@app.route("/sessions/challenges/storingState")
def hiddenState():


    username = flask.request.args.get("user")
    isAdmin = flask.request.args.get("admin",None)
    if username:
        if isAdmin is None:
            return flask.redirect(flask.url_for("hiddenState", user=username, admin=0))


    flag = "5067{State_Mangled_In_F0rms}"

    return flask.render_template("urlState.html",
                                 uName = username,
                                 admin = isAdmin,
                                 flag = flag
                                 )
 


