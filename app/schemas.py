# UNTUK BLUEPRINT / RESPONSE API
from pydantic import BaseModel

# -- User Schemas --
class UserBase(BaseModel):
    name: str
    job: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int


# -- Layer Schemas --
class LayerBase(BaseModel):
    layer_name: str
    lon: float
    lat: float