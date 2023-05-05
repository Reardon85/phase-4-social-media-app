from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to my social media app!'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)