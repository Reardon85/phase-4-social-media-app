from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt










following = db.Table('following',
                    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
                    )

class User(db.Model, SerializerMixin):
    __tablename__= 'users'

    serialize_rules= ('-_password_hash', '-following', '-followed_by', '-posts')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    avatar_url = db.Column(db.String, default='https://the-tea.s3.us-east-2.amazonaws.com/user_icon.png')
    bio = db.Column(db.String)
    last_request = db.Column(db.DateTime, default=datetime.utcnow)

    # posts relationship
    posts = db.relationship('Post', backref='user', lazy=True)
    # followers relationship
    following = db.relationship('User', 
                                secondary=following,
                                primaryjoin=(following.c.followed_id == id),
                                secondaryjoin=(following.c.follower_id == id),
                                backref=db.backref('followed_by',))
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )

    def active_recently(self):
        diff =  datetime.now() - self.last_request

        print("diff")
        print(diff)
        print("time delta")
        print(timedelta(minutes=2))
        if diff < timedelta(minutes=2):
            print("Active recently")
            return True
        else:
            return False
        
    def update_activity(self):
        self.last_request= datetime.now()
        db.session.add(self)
        db.session.commit()

    def logged_off(self):
        self.last_request = self.last_request + timedelta(minutes=100)

        print("logging off")
        db.session.add(self)
        db.session.commit()

    # @validates('password')
    # def validates_password(self, key, password):
    #     password_str = str(password)
    #     if len(password_str) != 7:
    #         raise ValueError('Password must be 7 characters')
    #     return password
    
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Must be valid email address")
        return email
    

    
    

class Post(db.Model, SerializerMixin):
    __tablename__= 'posts'

    serialize_rules= ('-user', '-likes', '-comments')

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    # user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # comments relationship
    comments = db.relationship('Comment', backref='post',)

    # likes relationship
    likes = db.relationship('Like', backref='post', )

    def like_count(self):
        return len(self.likes)
    
    def comment_count(self):
        return len(self.comments)




class Comment(db.Model, SerializerMixin):
    __tablename__= 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # post_id foreign key
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)




class Like(db.Model, SerializerMixin):
    __tablename__ = 'likes'
    serialize_rules = ('-user', '-post')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id'),)




# class Like(db.Model, SerializerMixin):
#     __tablename__ = 'likes'



#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     # user_id foreign key
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#     # post_id foreign key
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)



    def __repr__(self):
        return f"Like('{self.post_id}', '{self.user_id}')"
