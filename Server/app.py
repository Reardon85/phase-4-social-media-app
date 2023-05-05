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


if __name__ == '__main__':
    app.run(port=5555, debug=True)