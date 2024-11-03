# app/components/auth/services.py

import bcrypt
import jwt
from datetime import datetime, timedelta
from .models import User
import os
import logging

logger = logging.getLogger(__name__)

# Retrieve SECRET_KEY from environment variables for better security
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    logger.critical("SECRET_KEY environment variable not set.")
    raise ValueError("SECRET_KEY environment variable not set.")

# Token expiration settings
ACCESS_TOKEN_EXPIRY_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRY_HOURS", 1))
REFRESH_TOKEN_EXPIRY_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRY_DAYS", 7))

# Password Management

def hash_password(password):
    """
    Hashes a password using bcrypt.
    Args:
        password (str): The user's password.
    Returns:
        str: The hashed password.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    logger.debug("Password hashed successfully.")
    return hashed.decode('utf-8')


def check_password(hashed_password, password):
    """
    Checks if a provided password matches the hashed password.
    Args:
        hashed_password (str): The hashed password stored in the database.
        password (str): The password provided by the user.
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    try:
        match = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        if match:
            logger.debug("Password verification successful.")
        else:
            logger.debug("Password verification failed.")
        return match
    except Exception as e:
        logger.exception(f"Error verifying password: {e}")
        return False

# JWT Management

def create_access_token(user_id):
    """
    Creates a JWT access token for a user.
    Args:
        user_id (int): The ID of the user.
    Returns:
        str: The JWT access token.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRY_HOURS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    logger.debug(f"Access token created for user_id: {user_id}")
    return token


def create_refresh_token(user_id):
    """
    Creates a JWT refresh token for a user.
    Args:
        user_id (int): The ID of the user.
    Returns:
        str: The JWT refresh token.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    logger.debug(f"Refresh token created for user_id: {user_id}")
    return token


def decode_token(token):
    """
    Decodes a JWT token.
    Args:
        token (str): The JWT token to decode.
    Returns:
        dict: The decoded payload if the token is valid, None otherwise.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        logger.debug("Token decoded successfully.")
        return decoded
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token.")
        return None

# Authentication Service Functions

def register_user(data):
    """
    Registers a new user in the system.
    Args:
        data (dict): User data including username, password, confirm_password, and role.
    Raises:
        ValueError: If validation fails or username already exists.
    """
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    role = data.get('role')

    # Validation
    if not username or not password or not confirm_password or not role:
        logger.error("Registration failed: Missing required fields.")
        raise ValueError("All fields are required.")
    if password != confirm_password:
        logger.error("Registration failed: Passwords do not match.")
        raise ValueError("Passwords do not match.")
    if User.find_by_username(username):
        logger.error(f"Registration failed: Username '{username}' already exists.")
        raise ValueError("Username already exists.")

    try:
        hashed_password = hash_password(password)
        new_user = User(username=username, role=role)
        new_user.password_hash = hashed_password  # Set the password_hash directly
        new_user.save()
        logger.info(f"New user registered: {username}")
    except Exception as e:
        logger.exception(f"Error registering user '{username}': {e}")
        raise ValueError("Failed to register user due to a server error.")

def authenticate_user(username, password):
    """
    Authenticates a user by their username and password.
    Args:
        username (str): The username of the user trying to authenticate.
        password (str): The password provided by the user.
    Returns:
        User: The authenticated user if credentials are correct, None otherwise.
    """
    user = User.find_by_username(username)
    if user and user.verify_password(password):
        logger.debug(f"User '{username}' authenticated successfully.")
        return user
    logger.debug(f"Authentication failed for user '{username}'.")
    return None

def login_user(username, password):
    """
    Authenticates the user and provides access and refresh tokens.
    Args:
        username (str): The username of the user trying to log in.
        password (str): The password provided by the user.
    Returns:
        dict: A dictionary containing access and refresh tokens.
    Raises:
        ValueError: If authentication fails.
    """
    user = authenticate_user(username, password)
    if not user:
        logger.error(f"Login failed for user '{username}': Invalid credentials.")
        raise ValueError("Invalid username or password.")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    logger.info(f"User '{username}' logged in successfully.")
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user_role': user.role,
        'username': user.username
    }

def refresh_access_token(refresh_token):
    """
    Generates a new access token using a valid refresh token.
    Args:
        refresh_token (str): The JWT refresh token.
    Returns:
        str: A new access token if the refresh token is valid.
    Raises:
        ValueError: If the refresh token is invalid or expired.
    """
    decoded_token = decode_token(refresh_token)
    if decoded_token is None:
        logger.error("Token refresh failed: Invalid or expired refresh token.")
        raise ValueError("Invalid or expired refresh token.")

    user_id = decoded_token.get('user_id')
    new_access_token = create_access_token(user_id)
    logger.debug(f"Access token refreshed for user_id: {user_id}")
    return new_access_token