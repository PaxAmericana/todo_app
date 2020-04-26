from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique= True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #creates an "author" col in the Post model
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

