from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.security import authenticate_user, create_access_token, hash_password, get_current_user
from app.models.user import User
from app.schemas.user import UserLoginSchema, UserRegisterSchema, UserSchema
from app.core.settings import Settings
from app.api.deps import get_settings

router = APIRouter(tags=["auth"], prefix="/auth")

@router.post("/login", response_model=UserSchema)
async def login(
        user_data: UserLoginSchema,
        response: Response,
        db: Annotated[Session, Depends(get_db)],
        settings: Annotated[Settings, Depends(get_settings)]
):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.api.secured
    )
    return UserSchema.model_validate(user)

@router.post("/register", response_model=UserSchema)
async def register(
        user_data: UserRegisterSchema,
        db: Annotated[Session, Depends(get_db)]
):
    try:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        hashed_password = hash_password(user_data.password)
        user_dict = user_data.model_dump()
        user_dict["password"] = hashed_password
        new_user = User(**user_dict)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserSchema.model_validate(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return UserSchema.model_validate(current_user)

