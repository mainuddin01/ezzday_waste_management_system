# app/components/auth/utils.py

from typing import Optional
from starlette.requests import Request
from app.components.auth.models import User
from app.components.auth.services import decode_token

def get_current_user(req: Request) -> Optional[User]:
    """
    Retrieves the current user from the session using the access token.
    """
    access_token = req.session.get('access_token')
    if access_token:
        decoded_token = decode_token(access_token)
        if decoded_token:
            user_id = decoded_token.get('user_id')
            return User.find_by_id(user_id)
    return None