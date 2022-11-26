from pydantic import BaseModel


class ImageBase(BaseModel):
    image_name: str


class ImageAdd(ImageBase):
    ...


class Image(ImageAdd):
    id: int

    class Config:
        orm_mode = True
