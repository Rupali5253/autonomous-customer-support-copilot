from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(password)

    # Create user
    new_user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }

@router.post("/login")
def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    # Find user by email
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # User not found
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role
    }

@router.post("/create-agent")
def create_agent(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Only manager can create agents
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can create agents"
        )

    # Check if email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(password)

    # Create agent
    new_agent = User(
        name=name,
        email=email,
        password=hashed_password,
        role="agent"
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return {
        "message": "Agent created successfully",
        "agent_id": new_agent.id,
        "name": new_agent.name,
        "email": new_agent.email,
        "role": new_agent.role
    }

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Only manager can view all users
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can access user list"
        )

    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )

    return {
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at
            }
            for user in users
        ]
    }