
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()



metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)




followers = db.Table('followers',
                      db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                      )

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # posts relationship
    posts = db.relationship('Post', backref='user', lazy=True)
    # followers relationship
    followers = db.relationship('User', 
                                secondary=followers,
                                primaryjoin=(followers.c.followed_id == id),
                                secondaryjoin=(followers.c.follower_id == id),
                                backref=db.backref('followed_by',))

    @validates('password')
    def validates_password(self, key, password):
        password_str = str(password)
        if len(password_str) != 7:
            raise ValueError('Password must be 7 characters')
        return password
    
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Must be valid email address")
        return email
    
    

class Post(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # comments relationship
    comments = db.relationship('Comment', backref='post',)

    # likes relationship
    likes = db.relationship('Like', backref='post', )




class Comment(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # post_id foreign key
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)



class Like(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)

    # user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # post_id foreign key
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.post_id}', '{self.user_id}')"
