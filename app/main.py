from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from . import models  
from . import schemas  
from . import crud 
from .database import get_db, engine
from .auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_user_refresh_token,
    revoke_token,
    refresh_access_token,
    oauth2_scheme,
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# User signup endpoint
@app.post("/signup/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db=db, user=user)
    except Exception as e:  # Catch and log any exceptions
        print(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# User signin endpoint
@app.post("/signin/", response_model=schemas.Token)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user endpoint
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

# Revoke token endpoint
@app.post("/token/revoke/")
def revoke(current_user: schemas.User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    revoke_token(token)
    return {"msg": "Token revoked"}

# Refresh token endpoint
@app.post("/token/refresh/", response_model=schemas.Token)
def refresh_token(current_user: schemas.User = Depends(get_current_user_refresh_token)):
    new_token = refresh_access_token(current_user.email)
    return {"access_token": new_token, "token_type": "bearer"}
