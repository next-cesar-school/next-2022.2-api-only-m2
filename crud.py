import os
import glob
import re
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from model import Images
from PIL import Image
from imagehash import whash
# import schema

imagesdir = "images/"
comaparedir = "compare/"


def get_images(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Images).offset(skip).limit(limit).all()


def add_new_image(db: Session, file: UploadFile):

    directory = "images/"

    save_and_validate_image(file, directory=imagesdir)

    img_name = Images(
        image_name=file.filename
    )
    db.add(img_name)
    db.commit()
    db.refresh(img_name)

    for value in db.query(Images.id).distinct().order_by(Images.id.desc()).first():
        name_id = value

    rename_image(file=file, new=name_id, directory=imagesdir)

    return {"status": "Imagem enviada com sucesso"}


def get_image_by_id(db: Session, sl_id: int):

    return db.query(Images).filter(Images.id == sl_id).first()


def get_similar_image(db: Session, file: UploadFile):

    save_and_validate_image(file=file, directory=comaparedir)
    rename_image(file=file, new="temp", directory=comaparedir)

    if [f for f in os.listdir(imagesdir) if f.endswith(".jpeg")] == []:
        clear_compare()
        raise HTTPException(
            status_code=400, detail="O banco de imagens está vazio")

    hash_model = whash(Image.open(f"{comaparedir}temp.jpeg"))
    size = len(hash_model)
    more_similar = 0
    similar_file = None

    for image_file in os.listdir(imagesdir):
        if image_file.endswith(".jpeg"):
            hash_c = 100 - \
                (((hash_model -
                 whash(Image.open(f"{imagesdir}{image_file}"))) / size) * 100)

            if hash_c > more_similar:
                more_similar = hash_c
                similar_file = image_file

    number_l = [int(s) for s in re.findall(r'\b\d+\b', similar_file)]
    id_number = number_l[0]

    clear_compare()

    return get_image_by_id(db=db, sl_id=id_number)


def delete_image_by_id(db: Session, sl_id: int):

    try:
        db.query(Images).filter(Images.id == sl_id).delete()
        db.commit()

        os.remove(f"images\\{sl_id}.jpeg")
    except Exception as e:
        raise Exception(e)


def compare_two_images(files: list[UploadFile]):

    count = 1
    for file in files:
        save_and_validate_image(file, directory=comaparedir)
        rename_image(file=file, new=f"temp{count}", directory=comaparedir)
        count += 1
    count = 1

    first_hash = whash(Image.open(f"{comaparedir}temp1.jpeg"))
    second_hash = whash(Image.open(f"{comaparedir}temp2.jpeg"))
    size = len(first_hash)

    similarity = 100 - (((first_hash - second_hash) / size) * 100)

    clear_compare()

    return {"resultados": f"As imagens são {similarity}% semelhantes"}


def save_and_validate_image(file: UploadFile, directory: str):

    file_location = f"{directory}{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    try:
        img = Image.open(file_location)
        img.verify()
    except Exception:
        os.remove(file_location)
        clear_compare()
        raise HTTPException(status_code=400, detail="Arquivo corrompido")


def rename_image(file: UploadFile, new, directory: str):

    old_name = f"{directory}{file.filename}"
    new_name = f"{directory}{new}.jpeg"

    os.rename(old_name, new_name)


def clear_compare():
    for filename in os.listdir(comaparedir):
        if filename.endswith(".jpeg"):
            os.remove(os.path.join(comaparedir, filename))
