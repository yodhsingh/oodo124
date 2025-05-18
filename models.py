from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, date


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///synergyshere.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['JWT_SECRET_KEY'] = 'yodhsingh'
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    projects_created = db.relationship('Project', backref='creator', lazy=True)
    settings = db.relationship('Setting', backref='user', uselist=False)

class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship('ProjectMember', backref='project', lazy=True)
    tasks = db.relationship('Task', backref='project', lazy=True)
    comments = db.relationship('Comment', backref='project', lazy=True)

class ProjectMember(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String(50), default='member')

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship('TaskAssignment', backref='task', lazy=True)

class TaskAssignment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Setting(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notifications_enabled = db.Column(db.Boolean, default=True)



with app.app_context():
    db.create_all()
    if User.query.filter_by(email='singhadmin@gmail.com').first() is None:
        admin_password= generate_password_hash('penduwarrior')
        admin_dob = datetime.strptime('2002-08-17', '%Y-%m-%d').date()  # Convert to date
        admin = User(email='singhadmin@gmail.com',name='yodhsingh',password=admin_password,dob=admin_dob)
        db.session.add(admin)
        db.session.commit()
        print("User user created.")
    else:
        print('User already exits')