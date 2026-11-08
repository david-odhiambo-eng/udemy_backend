from fastapi import status, Depends, HTTPException, APIRouter
from app.schemas.users import (
    CreateUser,
    CreateUserResponse,
    LoginUser,
    LoginUserResponse,
)
from sqlalchemy.orm import Session
from app.db.db_connections import get_db
from app.db.users import User
from app.encrption.encrption import hash_password, verify_password
from app.encrption.jwt import create_access_token, restrict_route

auth_router = APIRouter(tags=["AUTHENTICATION"])


@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    # check if user is in our db
    user_db = db.query(User).filter(User.email == user.email).first()
    # if in db, raise error
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="USER ALREADY EXISTS"
        )
    # if not in db, create
    password = hash_password(user.password)
    new_user = User(player_name=user.player_name, email=user.email, password=password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return CreateUserResponse(email=new_user.email, player_name=new_user.player_name)


# SIGNING IN A USER


@auth_router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginUserResponse
)
def login_user(user: LoginUser, db: Session = Depends(get_db)):
    # 1. Check if user is in db
    user_db = db.query(User).filter(User.email == user.email).first()
    # 2. If not in db, raise error
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNATHORIZED"
        )
    # 3. If in db, check password matching
    password_match = verify_password(user.password, user_db.password)
    # 4. If password not matching, raise error
    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )
    # 5. If password matching, success
    access_token = create_access_token({"sub": str(user_db.id)})
    return LoginUserResponse(
        email=user_db.email,
        player_name=user_db.player_name,
        access_token=access_token,
        token_type="bearer",
    )


@auth_router.get("/check-login", status_code=status.HTTP_200_OK)
def check_logged_in_user(current_user=Depends(restrict_route)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )
    return current_user
