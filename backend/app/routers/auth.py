from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    get_db,
    require_admin,
)
from app.core.security import (
    create_access_token,
    decode_refresh_token,
)
from app.models.user import User
from app.models.user_session import UserSession
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
)

from app.services.auth_service import (
    authenticate_user,
    create_user_tokens,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# Admin Test


@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_admin),
):
    return {
        "message": "Admin access granted",
        "username": current_user.username,
        "role": current_user.role.code,
    }


# 
# Login
# 

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        username=login_data.username,
        password=login_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return create_user_tokens(
        db,
        user,
    )


# Refresh Access Token

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    
    
    # Validate refresh JWT


    try:
        employee_id = decode_refresh_token(
            refresh_data.refresh_token
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # 
    # Find stored session
    # 

    session = db.scalar(
        select(UserSession).where(
            UserSession.refresh_token
            == refresh_data.refresh_token
        )
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found",
        )

    # 
    # Check whether session was logged out
    # 

    if session.revoked_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has been logged out",
        )

    # 
    # Check session expiration
    # 

    if session.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )

    # 
    # Find user using Employee ID
    # 

    user = db.scalar(
        select(User).where(
            User.employee_id == employee_id
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # 
    # Check account status
    # 

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # 
    # Create new access token
    # 

    return {
        "access_token": create_access_token(
            user.employee_id
        ),
        "refresh_token": refresh_data.refresh_token,
        "token_type": "bearer",
    }


# 
# Logout
# 

@router.post("/logout")
def logout(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    # 
    # Find the session
    # 

    session = db.scalar(
        select(UserSession).where(
            UserSession.refresh_token
            == refresh_data.refresh_token
        )
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found",
        )

    # 
    # Check if already logged out
    # 

    if session.revoked_at is not None:
        return {
            "message": "Already logged out"
        }

    # 
    # Revoke session
    # 

    session.revoked_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Logged out successfully"
    }


# Current User


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "employee_id": current_user.employee_id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "designation": current_user.designation,
        "email": current_user.email,
        "role_id": current_user.role_id,
        "organization_unit_id": current_user.organization_unit_id,
        "is_active": current_user.is_active,
    }