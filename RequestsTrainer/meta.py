import flask

from jinja_markdown import MarkdownExtension
#from flask_httpauth import HTTPBasicAuth
import flask_httpauth

app = flask.Flask(__name__)
app.secret_key = "Sekr3t_Tok3n"
app.config.update(
    SESSION_COOKIE_SAMESITE='Strict',
)


app.jinja_env.add_extension(MarkdownExtension)


auth = flask_httpauth.HTTPBasicAuth()
bauth = flask_httpauth.HTTPTokenAuth()



    
