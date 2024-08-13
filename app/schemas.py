# UNTUK BLUEPRINT / RESPONSE API
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    job: str

class UserCreate(UserBase):
    username: str
    password: str

class User(UserBase):
    id: int
    username: str


# -- Layer Schemas --
class LayerBase(BaseModel):
    layer_name: str
    lon: float
    lat: float
