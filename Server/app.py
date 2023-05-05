from flask import Flask, request, make_response, abort, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Post, Comment, Like

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
api = Api(app)
db.init_app(app)


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to my social media app!'})

class Users(Resource):
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
            return make_response(new_u.to_dict(), 201)
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