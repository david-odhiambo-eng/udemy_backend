from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from settings.load_env import SECRET_KEY, ALGORITHM, ACCESS_TIME
from fastapi import HTTPException, status, Request, Depends
from sqlalchemy.orm import Session
from app.db.db_connections import get_db
from app.db.users import User


def create_access_token(data: dict):
    to_encode = data.copy()
    expiry_time = datetime.now(timezone.utc) + timedelta(days=float(ACCESS_TIME))
    to_encode.update({"exp": expiry_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    jwt_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = payload.get("sub")
        if id == None:
            raise jwt_error
        return id
    except JWTError:
        raise jwt_error


def restrict_route(request: Request, db: Session = Depends(get_db)):
    authorization_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
    )

    header = request.headers.get("Authorization")
    if not header:
        raise authorization_error

    parts = header.split()
    if len(parts) != 2:
        raise authorization_error
    bearer, access_token = parts

    if bearer.lower() != "bearer":
        raise authorization_error
    id = verify_token(token=access_token)

    user_db = db.query(User).filter(User.id == id).first()
    if not user_db:
        raise authorization_error

    return user_db
    
