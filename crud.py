from sqlalchemy.orm import Session
from fastapi import UploadFile
from model import Images
# import schema
import os


def get_images(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Images).offset(skip).limit(limit).all()


def add_new_image(db: Session, file: UploadFile):

    file_location = f"images/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    img_name = Images(
        image_name=file.filename
    )
    db.add(img_name)
    db.commit()
    db.refresh(img_name)

    for value in db.query(Images.id).distinct().order_by(Images.id.desc()).first():
        name_id = value

    old_name = f"images\\{file.filename}"
    new_name = f"images\\{name_id}.png"

    os.rename(old_name, new_name)

    return {"status": "image saved"}


def delete_image_by_id(db: Session, sl_id: int):

    try:
        db.query(Images).filter(Images.id == sl_id).delete()
        db.commit()

        os.remove(f"images\\{sl_id}.png")
    except Exception as e:
        raise Exception(e)


def get_image_by_id(db: Session, sl_id: int):

    return db.query(Images).filter(Images.id == sl_id).first()

    # def delete_image_by_id(db: Session, sl_id: int):

    #     try:
    #         db.query(model.Images).filter(model.Images.id == sl_id).delete()
    #         db.commit()
    #     except Exception as e:
    #         raise Exception(e)

    # def add_new_image(db: Session, image: schema.ImageAdd):

    #     details = model.Images(
    #         image_name=image.image_name,
    #         image_hash=image.image_hash,
    #         binary=image.binary
    #     )
    #     db.add(details)
    #     db.commit()
    #     db.refresh(details)

    #     db.identity_key

    #     return model.Images(**image.dict())
