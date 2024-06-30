from sqlalchemy.orm import Session
from . import models
from . import schemas
from .utils import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
