import os
from dotenv import load_dotenv
load_dotenv()
from flask import request, make_response, abort, jsonify, render_template, session
from flask_restful import  Resource
from sqlalchemy.exc import IntegrityError
from models import User, Post, Comment, Like
from config import app, db, api






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
        
        session['user_id'] = the_user.id
        return make_response(the_user.to_dict(), 200)
    
api.add_resource(Login, '/login')

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return make_response({'message': 'Successfully Logged Out'}, 204)

        return make_response({'error':"401 Unauthorized"}, 401)    


api.add_resource(Logout, '/logout')

class Users(Resource):
#I think the only time we'd use this is if we're implimenting a search feature for a specific user. Where we are letting the front end do the filtering.
# But if we do then we're only going to want to return a list of usernames. It would be bad practice to let anyone do a get request 
# that returns all our users passwords(even if they are hashed) and e-mails. will have to consider if want to do a search by username on frontend or backend.
#  backend faster but frontend will let us do am onchange filter.  
    def get(self):
        users_list = []
        for u in User.query.all():
            users_dict = {
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'password': u.password
            }
            users_list.append(users_dict)
        return make_response(users_list, 200)
    
    def post(self):
        data = request.get_json()
        new_u = Post(name = data['name'],
                    email = data['email'],
                    password = data['password'])
        try:
            db.session.add(new_u)
            db.session.commit()
            return make_response(new_u, 201)
        except Exception as ex:
            return make_response({'error': [ex.__str__()]}, 422)
    
api.add_resource(Users, '/users')

class UsersById(Resource):
    def get(self, id):
        u_instance = User.query.filter_by(id = id).first()
        if u_instance == None:
            return make_response({"error": "User not found"}, 404)
        return make_response(u_instance.to_dict(), 200)
    def delete(self, id):
        user = User.query.filter_by(id = id).first()
        if user == None:
            return make_response({"error": "User not found"}, 404)
        db.session.delete(user)
        db.session.commit()
        return make_response('Account deleted successfully', 200)
    
    def patch(self, id):
        user_instance = User.query.filter_by(id = id).first()
        if user_instance == None:
            return make_response({"errors": ["validation errors"]}, 404)
        data = request.get_json()
        for key in data.keys():
            setattr(user_instance, key, data[key])
        db.session.add(user_instance)
        db.session.commit()
        return make_response(user_instance.to_dict(), 202)

api.add_resource(UsersById, '/users/<int:id>')

class Posts(Resource):
#Shouldn't be an issue for our site. But for an actual social media site with millions of posts. You'd never be in a situation where you'd 
# send a browser request a list with millions of posts. Maybe when we get the "following" table working we alter this so it only returns first 100 posts
#from the people the user is following. Flask "session" will be storing the "user_id" so we don't need to pass it as parameter in the url. 
    def get(self):
        posts_list = []
        for p in Post.query.all():
            posts_dict = {
                'id': p.id,
                'image': p.image,
                'content': p.content,
                'date_posted': p.date_posted
            }
            posts_list.append(posts_dict)
        return make_response(posts_list, 200)
    
    def post(self):
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
#It's unlikely that we will run into a situation where we will need to return a list containing every comment from every post ever made.
#Comments will likely be pulled in similar way to how planets were were appended to scientist in  Scientist_by_ID get function in cosmic fun CC
# Since a commenet will only ever be displayed in connection to the post it lists as it's foreign key. 
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




if __name__ == '__main__':
    app.run(port=5555, debug=True)