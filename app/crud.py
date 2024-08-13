# CRUD (CREATE, READ, UPDATE, DELETE)
from sqlalchemy.orm import Session
from . import models, schemas

# -- USER API --
# Dapatkan semua user
def get_users(db: Session):
    return db.query(models.User).all()


# Create User
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, job=user.job)
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