from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from sqlalchemy.ext.orderinglist import ordering_list

@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique= True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #creates an "author" col in the Post model
    task_lists = db.relationship('TaskList', backref='author',lazy=True)

    # to get all the posts, it runs an additional query to gather all the posts in table "Post" with Author = User
    # note 'Post" is uppercase because it's referencing the Class (not the able.. tiny difference)
    def __repr__(self):
        return f'user({self.username}, {self.email}, {self.image_file})'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # note, if you passed in datetime.utcnow() with parenthesis
    # it would call the method and compute the current time at runtime rather than each time the class is instantiated
    # therefore, we need to pass the function itself as an argument
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #note user is lowercase because it's a table
    def __repr__(self):
        return f'user({self.title}, {self.date})'

class TaskList(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # note user is lowercase because it's a table
    tasks = db.relationship("Task", backref="TaskList", order_by="Task.order",
                           collection_class=ordering_list('order'))



class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer)
    TaskList_id = db.Column(db.Integer, db.ForeignKey(TaskList.id), nullable=False)  # note user is lowercase because it's a table
