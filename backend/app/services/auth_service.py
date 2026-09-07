from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.user import User
from app.models.user_session import UserSession


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User | None:
    user = db.scalar(
        select(User).where(
            User.username == username
        )
    )

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user


def create_user_tokens(
    db: Session,
    user: User,
) -> dict:
    access_token = create_access_token(user.employee_id)
    refresh_token = create_refresh_token(user.employee_id)

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    session = UserSession(
        employee_id=user.employee_id,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )

    db.add(session)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }