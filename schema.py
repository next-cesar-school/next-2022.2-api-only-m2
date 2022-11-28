from pydantic import BaseModel

# Criação de modelos de squema que podem ser usados para salvar
# detalhes de imagens no banco de dados e enviar respostas ao
# usuário


class ImageBase(BaseModel):
    image_name: str


class ImageRequest(ImageBase):
    ...


class ImageResponse(ImageRequest):
    id: int

    class Config:
        orm_mode = True
