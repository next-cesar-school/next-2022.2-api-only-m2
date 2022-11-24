from sqlalchemy.orm import Session
import model
import schema


def get_images(db: Session, skip: int = 0, limit: int = 100):

    return db.query(model.Images).offset(skip).limit(limit).all()


def get_image_by_id(db: Session, sl_id: int):

    return db.query(model.Images).filter(model.Images.id == sl_id).first()


def delete_image_by_id(db: Session, sl_id: int):

    try:
        db.query(model.Images).filter(model.Images.id == sl_id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)


def add_new_image(db: Session, image: schema.ImageAdd):

    details = model.Images(
        image_name=image.image_name,
        image_hash=image.image_hash,
        binary=image.binary
    )
    db.add(details)
    db.commit()
    db.refresh(details)
    return model.Images(**image.dict())