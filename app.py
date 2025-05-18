from flask import Flask, request, jsonify ,render_template, redirect ,url_for , flash , session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource, reqparse
import os
from flask_sqlalchemy import SQLAlchemy
from models import db,User
from datetime import datetime, date
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
    return render_template('login1.html')

@app.route("/signup")
def signup():
    return render_template("signup1.html")

@app.route('/signup', methods=['POST'])
def signup_post():
    name=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    dob_str = request.form.get('dob')
    dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
    password_hash = generate_password_hash(password)

    new_user= User(name=name, email=email, password=password_hash, dob=dob )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/login' , methods=['POST'])
def login_post():
    name=request.form.get('username')
    password=request.form.get('password')
    if not name or not password :
        flash('please fill out remaining field')
        return redirect(url_for('login'))
    user=User.query.filter_by(name=name).first()

    if not user:
        flash('useranmae does not exist')
        return redirect(url_for('login'))
    if not check_password_hash(user.password, password):
        flash('icorrect password')
        return redirect(url_for('login'))
    session['user_id'] = user.id
    flash('login succesfull')
    return redirect(url_for('layout'))    

@app.route("/layout")
def layout():
    return render_template("layout.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
