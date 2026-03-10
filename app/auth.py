import logging

from fastapi import HTTPException, Request, status
from .crud import get_user_by_username, verify_password
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        log.info("auth_user_not_found username=%s", username)
        return False
    if not verify_password(password, user.hashed_password):
        log.info("auth_invalid_password username=%s", username)
        return False
    return user


def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")
    return user
