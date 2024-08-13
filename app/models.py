# UNTUK RANGKA TABLE DATABASE
from sqlalchemy import Column, Integer, String, Float
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    name = Column(String(100))
    job = Column(String(100))


class Layer(Base):
    __tablename__ = 'layers'

    id = Column(Integer, primary_key=True, index=True)
    layer_name = Column(String(100))
    lon = Column(Float)
    lat = Column(Float)
