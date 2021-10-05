import flask

from jinja_markdown import MarkdownExtension
import flask_httpauth
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.secret_key = "Sup3r_SeKret_T0ken"
app.config.update(
    SESSION_COOKIE_SAMESITE='Strict',
    SQLALCHEMY_DATABASE_URI= 'sqlite:////tmp/test.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
)


app.jinja_env.add_extension(MarkdownExtension)


auth = flask_httpauth.HTTPBasicAuth()
bauth = flask_httpauth.HTTPTokenAuth()




        
