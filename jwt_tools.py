from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
import jwt_tools
import datetime
import os
import secrets
import base64
from functools import wraps
from dotenv import load_dotenv


# Simple function to generate a JWT secret key if it doesn't exist
def ensure_jwt_secret():
    if not os.getenv('SECRET_KEY'):
        # Generate a new key only if it doesn't exist
        random_bytes = secrets.token_bytes(64)
        secret_key = base64.urlsafe_b64encode(random_bytes).decode('utf-8')

        # Write to .env file
        try:
            with open('.env', 'a+') as env_file:
                env_file.seek(0)
                content = env_file.read()
                if 'SECRET_KEY=' not in content:
                    env_file.write(f"\nSECRET_KEY={secret_key}\n")
                    # Update environment for current process
                    os.environ['SECRET_KEY'] = secret_key
        except Exception:
            # Still update current environment even if file save fails
            os.environ['SECRET_KEY'] = secret_key

    return os.getenv('SECRET_KEY')