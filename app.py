from flask import Flask, request, jsonify ,render_template, redirect ,url_for , flash , session
from flask_restful import Api, Resource, reqparse
import os
from flask_sqlalchemy import SQLAlchemy
from models import db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///synergyshere.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

def get_db():
    return db

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

