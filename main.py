from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import crud
from model import Base
import schema
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

# Criação da aplicação do FastAPI
app = FastAPI()


# Função de auxílio para a ultiliação do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Requisição para retornar ao usuário todas as imagens salvas no
# banco de dados
@app.get("/get_all_images", response_model=list[schema.ImageResponse])
async def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = crud.get_images(db=db, skip=skip, limit=limit)
    return images


# Requisição que adiciona uma nova imagem na aplicação e salva
# o seu nome original no banco de dados
@app.post("/add_new_image")
async def add_new_image(file: UploadFile, db: Session = Depends(get_db)):

    extension_verifier(file=file)

    return crud.add_new_image(db=db, file=file)


# Requisição que retorna ao usuário uma imagem salva na
# aplicação que tenha a maior porcentagem de similaridade
# com a imagem enviada pelo usuário
@app.post("/get_similar_image", response_class=FileResponse)
def get_similar_image(file: UploadFile):

    extension_verifier(file=file)

    return crud.get_similar_image(file=file)


# Requisição que recebe duas imagens do usuário e retorna
# a porcentagem de similaridade entre as duas imagens
@app.post("/compare_two_images")
def compare_two_images(file1: UploadFile, file2: UploadFile):

    files = [file1, file2]

    for file in files:
        extension_verifier(file=file)

    return crud.compare_two_images(files=files)


# Deleta uma imagem da aplicação e suas informações do
# banco de dados com base no id recebido pelo usuário
@app.delete("/delete_image_by_id")
def delete_image_by_id(sl_id: int, db: Session = Depends(get_db)):
    details = crud.get_image_by_id(db=db, sl_id=sl_id)
    if not details:
        raise HTTPException(
            status_code=404, detail=f"Imagem não encontrada para ser removida")

    try:
        crud.delete_image_by_id(db=db, sl_id=sl_id)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Erro na remoção da imagem: {e}")

    return {"status": "Imagem removida com sucesso"}


# Função de auxílio que verifica as extensões de arquivos
# enviados pelos usuário
def extension_verifier(file: UploadFile):
    if not file.content_type == "image/jpeg":
        raise HTTPException(
            status_code=400, detail="Extensão de arquivo inválida."
        )
