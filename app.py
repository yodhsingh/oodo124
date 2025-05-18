from flask import Flask, request, jsonify ,render_template, redirect ,url_for , flash , session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource, reqparse
import os
from flask_sqlalchemy import SQLAlchemy
from models import db,User,Project
from datetime import datetime, date
app = Flask(__name__)
# Set a secret key for session management
app.secret_key = 'a8f5f167f44f4964e6c998dee827110c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///synergyshere.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.environ.get('SECRET_KEY', 'fallback_dev_key')
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
        flash('incorrect password')
        return redirect(url_for('login'))
    session['user_id'] = user.id
    flash('login succesfull')
    return redirect(url_for('layout'))    

@app.route("/layout")
def layout():
    project = Project.query.all()
    return render_template("layout.html",projects=project)
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
