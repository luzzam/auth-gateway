import os
import jwt
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'both username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'invalid username or password'}), 401

    token = jwt.encode({'id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Hello, {}'.format(payload['id'])}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)