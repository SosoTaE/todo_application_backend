from flask import request, jsonify
import jwt
import datetime



def authenticate_request(config):
    # Skip authentication for login route and other public routes
    if request.path == '/api/login':
        return None

    # Get token from Authorization header
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

    if not token:
        return jsonify({'message': 'Authentication token is missing'}), 401

    try:
        # Decode token
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])

        # Check if token is expired
        exp_timestamp = payload['exp']
        now = datetime.datetime.utcnow().timestamp()
        if now > exp_timestamp:
            return jsonify({'message': 'Token has expired'}), 401

        # Set user information to g object for access in route handlers
        g = request.environ.setdefault('werkzeug.request', {})
        g.user = {
            'username': payload['username'],
            'is_admin': payload.get('is_admin', False)
        }

    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except Exception as e:
        return jsonify({'message': f'Token validation error: {str(e)}'}), 401

    # Continue processing the request
    return None
