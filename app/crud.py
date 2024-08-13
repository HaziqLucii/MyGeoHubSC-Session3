# CRUD (CREATE, READ, UPDATE, DELETE)
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

# -- USER API --
# Dapatkan semua user
def get_users(db: Session):
    return db.query(models.User).all()


# Create User
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        name=user.name,
        job=user.job
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



# Dapatkan individual user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# Untuk update maklumat individu
def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.job = user.job
        db.commit()
        db.refresh(db_user)
    return db_user


# Untuk padam maklumat individu
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# -- Layer API --
# Dapatkan semua data layer
def get_layers(db: Session):
    return db.query(models.Layer).all()


# -- Security --
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
