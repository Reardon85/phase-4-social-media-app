import os
from uuid import uuid4
import boto3
from dotenv import load_dotenv
load_dotenv()
from flask import request, make_response, abort, jsonify, render_template, session
from flask_restful import  Resource
from sqlalchemy.exc import IntegrityError
from models import User, Post, Comment, Like, following, Notification
from config import app, db, api, asc, desc



@app.route('/notification')
def get_notifications():
    the_user =User.query.filter_by(id=session['user_id']).first()
    the_user.update_activity()

    notifications = Notification.query.filter_by(receiving_user_id=session['user_id']).order_by(desc(Notification.created_date)).limit(8).all()
    notification_list = []
    for notification in notifications:
        image = ''
        if notification.post_id:
            print(notification.post_id)
            post = Post.query.filter_by(id=notification.post_id).first()
            image = post.image

        notification_dict = {
            **notification.to_dict(),
            **notification.giver.to_dict(only=('avatar_url', 'username' )),
            'image': image
        }
        notification_list.append(notification_dict)
        notification.seen = True
        db.session.add(notification)

    db.session.commit()
    return make_response(notification_list, 200)
    



@app.route('/create-post', methods=['POST'])
def upload_image():
    file = request.files['image']
    content = request.values['content']

    s3 = boto3.resource('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    bucket = s3.Bucket('the-tea')

    bucket.put_object(Key=file.filename, Body=file)
  


    file_url = f"https://{bucket.name}.s3.amazonaws.com/{file.filename}"

    the_user =User.query.filter_by(id=session['user_id']).first()
    the_user.update_activity()

    new_posts = Post(user_id=the_user.id, content=content, image=file_url)
    db.session.add(new_posts)
    db.session.commit()
    return 'Image uploaded successfully!'


class Update_Profile(Resource):
    def get(self):
        the_user =User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        return make_response(the_user.to_dict(only=('avatar_url', 'bio', 'email')))
        


    def patch(self):
        the_user =User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        if request.values['fileExists'] == 'true':
            print(request.values['fileExists'])
            file = request.files['image']
            s3 = boto3.resource('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
            bucket = s3.Bucket('the-tea')
            test = bucket.put_object(Key=file.filename, Body=file)
            file_url = f"https://{bucket.name}.s3.amazonaws.com/{file.filename}"
        else:
            file = None

        if  not(request.values['currentPassword'] == 'null') and not(request.values['newPassword'] == 'null'):

            if the_user.authenticate(request.values['currentPassword']):
                the_user.password_hash = request.values['newPassword']
                db.session.add(the_user)
                db.session.commit()





        bio = request.values['bio']
        email = request.values['email']
        


        if file:
            the_user.avatar_url = file_url
        
        the_user.bio = bio
        the_user.email = email

        db.session.add(the_user)
        db.session.commit()
        return 'Image uploaded successfully!'

api.add_resource(Update_Profile, '/update-profile')





@app.route('/')
@app.route('/<int:id>')
def index(id=0):
    return render_template("index.html")


class Signup(Resource):
    def post(self):
        try:
            data = request.get_json()
            new_user = User(username=data.get('username'), email=data.get('email'))
            new_user.password_hash = data.get('password')
            
            db.session.add(new_user)
            db.session.commit()
            
            session['user_id'] = new_user.id
            return make_response(new_user.to_dict(), 201)
        except IntegrityError:
            return make_response({'error': '422 Unprocessable Entity'}, 422)
api.add_resource(Signup, '/signup')

class CheckSession(Resource):
    def get(self):

        if not session['user_id']:
            return make_response({'error': ' test 401 Unauthorized'}, 401)
        


        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()
        return make_response(the_user.to_dict(), 200)
api.add_resource(CheckSession, '/check_session')
    
class Login(Resource):
    def post(self):

        data = request.get_json()

        the_user = User.query.filter_by(username=data.get('username')).first()
        
        if not the_user:
            return make_response({'error':'username does not exist'}, 404)
        
        if not the_user.authenticate(data.get('password')):
            return make_response({'error:': 'Invalid Password'}, 400)
        
        the_user.update_activity()
        session['user_id'] = the_user.id
        return make_response(the_user.to_dict(), 200) 
api.add_resource(Login, '/login')

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            the_user = User.query.filter_by(id=session['user_id']).first()
            the_user.logged_off()
            session['user_id'] = None
            return make_response({'message': 'Successfully Logged Out'}, 204)

        return make_response({'error':"401 Unauthorized"}, 401)    
api.add_resource(Logout, '/logout')


class Users(Resource):
    def get(self):

        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()
        users = [{**user.to_dict(only=("id", "avatar_url", "username")), **{'active':user.active_recently()}} for user in User.query.all()]
        total = len(users)
        total_dict = {"total": total, "users": users}
        return make_response(total_dict, 200)
api.add_resource(Users, '/users')

class Users_By_Id(Resource):
    def get(self, id):
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        print(the_user.notifications_received)

        am_following = [False, False]
        profile_user = User.query.filter_by(id = id).first()
        if profile_user == None:
            return make_response({"error": "User not found"}, 404)
        
        if profile_user.id == session['user_id']:
            am_following = [True, True]
        else:
            am_following[0] = False
            following = [follow.id for follow in the_user.following]

            if id in following:
                am_following[1] = True

        profile_dict = {
            'profile_info': {
                'username': profile_user.username,
                'avatar_url': profile_user.avatar_url,
                'bio': profile_user.bio,
                'posts':len(profile_user.to_dict(only=("posts",))['posts']),
                'following':len(profile_user.to_dict(only=("following",))['following']),
                'followers':len(profile_user.to_dict(only=("followed_by",))['followed_by']),
                'active':profile_user.active_recently()
            },
            'posts': [post.to_dict(rules=('like_count', 'comment_count')) for post in profile_user.posts],
            # profile_user.to_dict(only=("posts",))['posts'],
            'am_following': am_following
        }   
        return make_response(profile_dict, 200)
    
    def delete(self, id):
        user = User.query.filter_by(id = id).first()
        if user == None:
            return make_response({"error": "User not found"}, 404)
        db.session.delete(user)
        db.session.commit()
        return make_response('Account deleted successfully', 200)
    
    def patch(self, id):
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()
        user_instance = User.query.filter_by(id = id).first()
        if user_instance == None:
            return make_response({"errors": ["validation errors"]}, 404)
        data = request.get_json()
        for key in data.keys():
            setattr(user_instance, key, data[key])
        db.session.add(user_instance)
        db.session.commit()
        return make_response(user_instance.to_dict(), 202)
api.add_resource(Users_By_Id, '/users/<int:id>')



class Home_Results(Resource):
    def get(self, total):
        posts_list = []
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        

        user_id = session['user_id']

        posts = Post.query.join(following, (following.c.follower_id == Post.user_id)).outerjoin(Like, Like.post_id == Post.id) \
        .filter(following.c.followed_id == user_id).group_by(Post.id).order_by(db.func.count(Like.id).desc()).all()

        more_posts = total < len(posts)
        print(more_posts)
        if not more_posts:
            total = len(posts) -1

        posts = posts[0:total]

        post_dicts = [post.to_dict(rules=('like_count',)) for post in posts]

        for post in post_dicts:
            user = User.query.filter_by(id=post['user_id']).first()
            user_dict = user.to_dict(only=('avatar_url', 'username'))
            liked = Like.query.filter_by(post_id=post['id']).filter_by(user_id=session['user_id']).first()

            like_dict = {
                'liked': (not liked == None)
            }
            

            temp = {**post, **user_dict, **like_dict}
            posts_list.append(temp)

        return_dict = {'posts':posts_list, 'more_posts': more_posts}    
        return make_response(return_dict, 200)
api.add_resource(Home_Results, '/home/<int:total>')

class Home_ForYou(Resource):
    def get(self, total):
        posts_list = []
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        

        user_id = session['user_id']

        posts = Post.query.join(Like, Like.post_id == Post.id).group_by(Post.id).order_by(db.func.count(Like.id).desc()).limit(100).all()

        more_posts = total < len(posts)
        print(more_posts)
        if not more_posts:
            total = len(posts) -1

        posts = posts[0:total]

        post_dicts = [post.to_dict(rules=('like_count', 'comment_count', )) for post in posts]

        for post in post_dicts:
            user = User.query.filter_by(id=post['user_id']).first()
            user_dict = user.to_dict(only=('avatar_url', 'username', '-id'))
            liked = Like.query.filter_by(post_id=post['id']).filter_by(user_id=session['user_id']).first()
            

            like_dict = {
                'liked': (not liked == None)
            }
            

            temp = {**post, **user_dict, **like_dict}
            posts_list.append(temp)

        return_dict = {'posts':posts_list, 'more_posts': more_posts}    
        return make_response(return_dict, 200)
api.add_resource(Home_ForYou, '/homeforyou/<int:total>')

class Posts(Resource):    
    def post(self):

        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        data = request.get_json()
        post = Post(image = data['image'],
                    content = data['content'],
                    user_id = data['user_id'])
        try:
            db.session.add(post)
            db.session.commit()
            return make_response(post.to_dict(), 201)
        except Exception as ex:
            return make_response({'error': [ex.__str__()]}, 422)
api.add_resource(Posts, '/posts')


class PostsById(Resource):
    def get(self, id):
        post = Post.query.filter_by(id = id).first()
        my_post = False
        if post == None:
            return make_response({"error": "Post not found"}, 404)
        
        if post.user_id == session['user_id']:
            my_post = True
        

        liked = Like.query.filter_by(post_id=id).filter_by(user_id=session['user_id']).first()

        like_dict = {
            'liked': (not liked == None)
        }
        
        user_dict = {
            'avatar_url': post.user.avatar_url,
            'username': post.user.username,
            'my_post': my_post
        }
        
        
        return make_response({**post.to_dict(rules=('like_count',)), **like_dict, ** user_dict}, 200)

    def delete(self, id):
        post = Post.query.filter_by(id = id).first()
        if post == None:
            return make_response({"error": "Post not found"}, 404)
        db.session.delete(post)
        db.session.commit()
        return make_response('Post deleted successfully', 200)
    
api.add_resource(PostsById, '/posts/<int:id>')

class Comments(Resource):
    def post(self):
        data = request.get_json()
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        try:
            comment = Comment(content = data['text'], post_id=data['postId'], user_id= session['user_id'])
            db.session.add(comment)
            db.session.commit()
            add_notification(type=2, the_user=the_user, receiving_user_id=comment.post.user_id, post_id=data['postId'])
            return make_response({**comment.to_dict(), **the_user.to_dict(only=('avatar_url', 'username'))}, 201)
        except Exception as ex:
            return make_response({'error': [ex.__str__()]}, 422)
api.add_resource(Comments, '/comments')

class CommentsById(Resource):
    def get(self, id):

        test = Comment.query.all()
        print(test)
        
        comments_list =[{**comment.to_dict(), **comment.user.to_dict(only=('avatar_url', "username")) } for comment in Comment.query.filter(Comment.post_id == id).all()]

        return make_response(comments_list, 200)
    
    def delete(self, id):
        comment = Comment.query.filter_by(id = id).first()
        if comment == None:
            return make_response({"error": "Comment not found"}, 404)
        db.session.delete(comment)
        db.session.commit()
        return make_response('Comment deleted successfully', 200)    
api.add_resource(CommentsById, '/comments/<int:id>')


class Follows(Resource):
    def post(self):
        follow_id = request.get_json()['userId']

        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()
        follow_user = User.query.filter_by(id=follow_id).first()

        the_user.following.append(follow_user)

        db.session.commit()

        add_notification(type=1, the_user=the_user, receiving_user_id=follow_id)
        return make_response(follow_user.to_dict(only=('username', 'id')), 201)
api.add_resource(Follows, '/follow')



class Follow_By_Id(Resource):
    def delete(self, id):
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()
        follow_user = User.query.filter_by(id=id).first()

        the_user.following.remove(follow_user)
        db.session.commit()
api.add_resource(Follow_By_Id, '/follow/<int:id>')





class Likes_By_Id(Resource):
    def post(self, id):
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        like_obj = Like(user_id = session['user_id'], post_id = id)
        db.session.add(like_obj)
        db.session.commit()

        
        add_notification(type=0, the_user=the_user, receiving_user_id=like_obj.post.user_id, post_id=id)
        return make_response(like_obj.to_dict(), 201)

    def delete(self, id):
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        like_obj = Like.query.filter_by(post_id=id).filter_by(user_id=session['user_id']).first()

        if not like_obj:
            return make_response({"error":"Like obj doesn't exist"}, 404)
        db.session.delete(like_obj)
        db.session.commit()

        return make_response({"message":"Like Successfully Deleted"}, 204)
api.add_resource(Likes_By_Id, '/likes/<int:id>')



@app.route('/active-notifications')
def active_notfication():

    notification = Notification.query.filter_by(receiving_user_id=session['user_id']).filter_by(seen=False).first()

    if notification:
        return make_response({'active': True}, 200)
    
    return make_response({'active': False}, 200)


def add_notification(type, the_user, receiving_user_id, post_id=False):

    action_list = [
        " liked your photo ",
        ' started following you ',
        ' commented on your photo '
    ]

    if not the_user.id == receiving_user_id:
        if post_id:
            new_notification = Notification(
                receiving_user_id= receiving_user_id,  
                action_user_id= session['user_id'],  
                post_id= post_id, 
                action= action_list[type], 
                seen= False       
            )
        else: 
            new_notification = Notification(
                receiving_user_id= receiving_user_id,  
                action_user_id= session['user_id'],   
                action= action_list[type], 
                seen= False
            )     




        db.session.add(new_notification)
        db.session.commit()



if __name__ == '__main__':
    app.run(port=5555, debug=True)