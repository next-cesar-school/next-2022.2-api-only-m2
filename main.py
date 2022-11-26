from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session

import crud
from model import Base
import schema
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get_all_images", response_model=list[schema.Image])
async def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = crud.get_images(db=db, skip=skip, limit=limit)
    return images


@app.post("/add_new_image")
async def add_new_image(file: UploadFile, db: Session = Depends(get_db)):

    extension_verifier(file=file)

    return crud.add_new_image(db=db, file=file)


@app.post("/get_similar_image", response_model=schema.Image)
def get_similar_image(file: UploadFile, db: Session = Depends(get_db)):

    extension_verifier(file=file)

    return crud.get_similar_image(db=db, file=file)


@app.post("/compare_two_images")
def compare_two_images(files: list[UploadFile]):

    for file in files:
        extension_verifier(file=file)

    return crud.compare_two_images(files=files)


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


def extension_verifier(file: UploadFile):
    if not file.content_type == "image/jpeg":
        raise HTTPException(
            status_code=400, detail="Extensão de arquivo inválida."
        )


# Adicionar lógica para válidação de arquivos
# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}
# @app.post("/uploadfile/")
# async def create_upload_file(
#     file: UploadFile = File(description="A file read as UploadFile")
# ):
#     return {"filename": file.filename}
# @app.get("/retrieve_all_images", response_model=List[schema.Image])
# def retrieve_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     images = crud.get_images(db=db, skip=skip, limit=limit)
#     return images
# @app.post("/add_new_image", response_model=schema.ImageAdd)
# def add_new_image(image: schema.ImageAdd, db: Session = Depends(get_db)):
#     return crud.add_new_image(db=db, image=image)
# @app.delete("/delete_image_by_id")
# def delete_image_by_id(sl_id: int, db: Session = Depends(get_db)):
#     details = crud.get_image_by_id(db=db, sl_id=sl_id)
#     if not details:
#         raise HTTPException(status_code=404, detail=f"No record found to delete")
#     try:
#         crud.delete_image_by_id(db=db, sl_id=sl_id)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
#     return {"delete status": "success"}
