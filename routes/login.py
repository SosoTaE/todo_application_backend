import datetime

import jwt

from flask import request, jsonify

def login(config):
    data = request.get_json()

    # Check if required fields exist
    if not data or not all(k in data for k in ('username', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    username = data['username']
    password = data['password']

    # Get credentials from environment variables
    expected_username = config.ADMIN_USERNAME
    expected_password_hash = config.ADMIN_HASHED_PASSWORD

    # Verify credentials
    if username != expected_username:
        # To avoid username enumeration, use a generic error
        return jsonify({'message': 'Invalid credentials'}), 401

    # Verify password
    if not password == expected_password_hash:
        return jsonify({'message': 'Invalid credentials'}), 401

    try:
        # Generate JWT token
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, config.SECRET_KEY, algorithm="HS256")

        return jsonify({
            'message': 'Login successful',
            'token': token
        }), 200

    except Exception as e:
        return jsonify({'message': f'Error during login: {str(e)}'}), 500
