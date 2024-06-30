from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import crud
from .database import get_db
from . import schemas

# Secret key and algorithm for JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Set of fake revoked tokens (in-memory storage)
fake_revoked_tokens = set()


def verify_password(plain_password, hashed_password):
    """Verify plain password against hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Generate hash for a given password."""
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    """Authenticate user based on email and password."""
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create access token with optional expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception, refresh_token_status):
    """Verify the validity of the access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if (email is None) or (token in fake_revoked_tokens and refresh_token_status == False):
            raise credentials_exception
        token_data = schemas.TokenData(id=str(email))
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Get current user based on the access token."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception, refresh_token_status=False)
    user = crud.get_user_by_email(db, email=token_data.id)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_user_refresh_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Get current user based on the refresh token."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception, refresh_token_status=True)
    user = crud.get_user_by_email(db, email=token_data.id)
    if user is None:
        raise credentials_exception
    
    return user

def revoke_token(token: str):
    """Revoke a given token by adding it to the set of revoked tokens."""
    fake_revoked_tokens.add(token)

def refresh_access_token(email: str):
    """Refresh access token for a given email."""
    new_token = create_access_token(data={"sub": email})
    return new_token
