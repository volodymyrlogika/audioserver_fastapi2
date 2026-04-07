from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "19109197bd5e7c289b92b2b355083ea26c71dee2085ceccc19308a7291b2ea06"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CryptContext - це клас, який використовується для управління хешуванням паролів.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def token_create(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



