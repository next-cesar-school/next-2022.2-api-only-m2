from typing import Optional
from pydantic import BaseModel


class ImageBase(BaseModel):
    image_name: str
    


class ImageAdd(ImageBase):
    image_hash: str
    binary: str


    class Config:
        orm_mode = True


class Image(ImageAdd):
    id: int

    class Config:
        orm_mode = True