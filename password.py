from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv, set_key

def hash_password_and_save_to_env(username, password, env_file='.env'):
    """
    Hash a password and save both the username and hashed password to .env file

    Args:
        username (str): Username to save
        password (str): Raw password to hash and save
        env_file (str): Path to .env file
    """
    # Generate password hash using Werkzeug
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Create .env file if it doesn't exist
    if not os.path.exists(env_file):
        open(env_file, 'a').close()

    # Load current .env file
    load_dotenv(env_file)

    # Update or create variables in the .env file
    set_key(env_file, 'USERNAME', username)
    set_key(env_file, 'PASSWORD', password_hash)

    print(f"Username and password hash saved to {env_file}")