from flask_sqlalchemy import SQLAlchemy

import app.meta as meta

db = SQLAlchemy(meta.app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.Text)
    category = db.Column(db.Text)
    hidden = db.Column(db.Boolean, default=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    level = db.Column(db.Text, default="user")
    
db.create_all()
