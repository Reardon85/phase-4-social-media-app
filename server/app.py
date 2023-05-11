import os
from uuid import uuid4
import boto3
from dotenv import load_dotenv
load_dotenv()
from flask import request, make_response, abort, jsonify, render_template, session
from flask_restful import  Resource
from sqlalchemy.exc import IntegrityError
from models import User, Post, Comment, Like, following
from config import app, db, api



s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


BUCKET_NAME = "the-tea"


@app.route("/aws-url", methods=["POST"])
def get_upload_url():
    content_type = request.json.get("content_type")
    if not content_type:
        return jsonify({"error": "No content type provided"}), 400

    # Generate a random file name
    file_name = f"{uuid4()}"

    # Generate a pre-signed URL
    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET_NAME, "Key": file_name, "ContentType": content_type},
        ExpiresIn=3600,  # URL expires in 1 hour
    )

    response = {
        "message": "Pre-signed URL generated successfully",
        "upload_url": url,
        "file_url": f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}",
    }
    return jsonify(response), 200







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
        print("following:")
        print(the_user.following)
        print("Followed by")
        print(the_user.followed_by)
        print(the_user.avatar_url)
        print(the_user.bio)
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
            'posts': profile_user.to_dict(only=("posts",))['posts'],
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
        p_instance = Post.query.filter_by(id = id).first()
        if p_instance == None:
            return make_response({"error": "Post not found"}, 404)
        return make_response(p_instance.to_dict(), 200)
# do we need to get a post by id?
# - Good point. I guess it depends on how we impliment the whole clicking on a post and making it bigger thing?
# But you're right, if they are clicking on the post then that means react already has the post's information. 

    def delete(self, id):
        post = Post.query.filter_by(id = id).first()
        if post == None:
            return make_response({"error": "Post not found"}, 404)
        db.session.delete(post)
        db.session.commit()
        return make_response('Post deleted successfully', 200)
    
api.add_resource(PostsById, '/posts/<int:id>')

class Comments(Resource):
    def get(self):
        comments_list = []
        for c in Comment.query.all():
            comments_dict = {
                'id': c.id,
                'content': c.content,
                'date_commented': c.date_commented
            }
            comments_list.append(comments_dict)
        return make_response(comments_list, 200)
    
    def post(self):
        the_user = User.query.filter_by(id=session['user_id']).first()
        the_user.update_activity()

        data = request.get_json()
        comment = Comment(content = data['content'])
        try:
            db.session.add(comment)
            db.session.commit()
            return make_response(comment.to_dict(), 201)
        except Exception as ex:
            return make_response({'error': [ex.__str__()]}, 422)
api.add_resource(Comments, '/comments')

class CommentsById(Resource):
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



if __name__ == '__main__':
    app.run(port=5555, debug=True)