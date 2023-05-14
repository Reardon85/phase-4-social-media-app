from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt











following = db.Table('following',
                    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
                    )



class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'

    serialize_rules= ('-receiver', '-giver', '-post')


    id = db.Column(db.Integer, primary_key=True)
    receiving_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    action = db.Column(db.String)
    seen = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class Conversation(db.Model, SerializerMixin):
    __tablename__ = 'conversations'

    serialize_rules=('-messages',)

    id = db.Column(db.Integer, primary_key=True)
    user_one_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_two_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    messages = db.relationship('Message', backref='conversation', cascade="all, delete, delete-orphan")

class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"

    serialize_rules=('-conversation',)

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default = db.func.now())






class User(db.Model, SerializerMixin):
    __tablename__= 'users'

    serialize_rules= ('-_password_hash', '-following', '-followed_by', '-posts', '-comments', '-notification_received', '-notification_given', '-conversations')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    avatar_url = db.Column(db.String, default='https://the-tea.s3.us-east-2.amazonaws.com/user_icon.png')
    bio = db.Column(db.String)
    last_request = db.Column(db.DateTime, default=datetime.utcnow)

    # conversations = db.relationship("Conversation", foreign_keys=[Conversation.user_one_id, Conversation.user_two_id])

    notifications_received = db.relationship('Notification', 
                                             foreign_keys='Notification.receiving_user_id', 
                                             backref='receiver', 
                                             lazy=True)
    notifications_given = db.relationship('Notification', 
                                             foreign_keys='Notification.action_user_id', 
                                             backref='giver', 
                                             lazy=True)
    
    # conversations = db.relationship()

    comments = db.relationship('Comment', backref='user')
    # posts relationship
    posts = db.relationship('Post', backref='user', lazy=True)
  
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

    serialize_rules= ('-user', '-likes', '-comments', '-notifications')

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    # user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # comments relationship
    comments = db.relationship('Comment', backref='post', cascade='all, delete, delete-orphan')

    # likes relationship
    likes = db.relationship('Like', backref='post', cascade='all, delete, delete-orphan' )

    notifications = db.relationship('Notification', 
                                             foreign_keys='Notification.post_id', 
                                             backref='post', 
                                             lazy=True,
                                             cascade='all, delete, delete-orphan')


    def like_count(self):
        return len(self.likes)
    
    def comment_count(self):
        return len(self.comments)




class Comment(db.Model, SerializerMixin):
    __tablename__= 'comments'
 
    serialize_rules= ('-post', '-user')

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



