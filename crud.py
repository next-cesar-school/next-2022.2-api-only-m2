from os import rename, remove, listdir, path
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from model import Images
from PIL import Image
from imagehash import whash
from shutil import move

# Constantes que representam os diretórios onde imagens são salvas
IMAGES_DIR = "images/"
COMPARE_DIR = "compare/"


# Retorna ao usuário uma lista de imagens do banco de dados com o
# nome original da imagem e seu id
def get_images(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Images).offset(skip).limit(limit).all()


# Adiciona uma nova imagem na aplicação e no banco de dados. Se a
# imagem for corrompida ou está em um formato diferente de jpeg,
# a imagem não é salva
def add_new_image(db: Session, file: UploadFile):

    # Salva e valida a imagem
    save_and_validate_image(file, directory=COMPARE_DIR)

    # Adiciona o nome original da imagem no banco de dados
    img_name = Images(
        image_name=file.filename
    )
    db.add(img_name)
    db.commit()
    db.refresh(img_name)

    # Coleta do último id gerado pelo banco de dados
    id_name = db.query(Images.id).distinct().order_by(Images.id.desc()).first()

    # Renomeia imagem com o id coletado
    rename_image(file=file, new=id_name[0])

    # Move a imagem do diretório compare para o de images
    move(f"{COMPARE_DIR}{id_name[0]}.jpeg", f"{IMAGES_DIR}{id_name[0]}.jpeg")

    return {"status": "Imagem enviada com sucesso"}


# Retorna a imagem salva no banco do dados pelo parametro sl_id
def get_image_by_id(db: Session, sl_id: int):

    return db.query(Images).filter(Images.id == sl_id).first()


# Recebe uma imagem do usuário e retorna uma imagem salva com a
# maior porcentagem de similaridade. Se a imagem for corrompida
# ou está em um formato diferente de jpeg, a imagem não é salva
def get_similar_image(file: UploadFile):

    # Salva e valida a imagem
    save_and_validate_image(file=file, directory=COMPARE_DIR)

    # Renomeia imagem para temp
    rename_image(file=file, new="temp")

    # Verificação de se o diretório images está vazio. Uma
    # Uma HTTPException é levantada para o usuário
    if [f for f in listdir(IMAGES_DIR) if f.endswith(".jpeg")] == []:
        clear_compare()
        raise HTTPException(
            status_code=400, detail="O banco de imagens está vazio")

    # Calculo para determinar o hash da imagem enviada pelo
    # usuário
    hash_model = whash(Image.open(f"{COMPARE_DIR}temp.jpeg"))
    size = len(hash_model)
    more_similar = 0
    similar_file = None

    # Iteração feita no diretório images para o calculo do
    # hash e coleta da imagem com maior porcentagem de
    # semelhança
    for image_file in listdir(IMAGES_DIR):
        if image_file.endswith(".jpeg"):
            hash_compare = 100 - \
                (((hash_model -
                 whash(Image.open(f"{IMAGES_DIR}{image_file}"))) / size) * 100)

            if hash_compare > more_similar:
                more_similar = hash_compare
                similar_file = image_file

    # As imagens do diretório compare são removidas
    clear_compare()

    return f"{IMAGES_DIR}{similar_file}"


# Recebe um id do usuário e romove uma imagem da aplicação e
# do banco de dados. Se o id passado pelo usuário não constar
# no banco, uma HTTPException é emviada ao usuário
def delete_image_by_id(db: Session, sl_id: int):

    try:
        db.query(Images).filter(Images.id == sl_id).delete()
        db.commit()

        remove(f"images\\{sl_id}.jpeg")
    except Exception as e:
        raise Exception(e)


# Comparação de duas imagens enviadas pelo usuário e retorna
# uma mensagem com a porcentagem de semelhança entre as duas
# imagens. Se as imagens forem corrompidas ou estão em um
# formato diferente de jpeg, as imagens não serão comparadas
def compare_two_images(files: list[UploadFile]):

    # As imagens são armazenadas no diretório compare e são
    # renomeadas para temp1 e temp2
    count = 1
    for file in files:
        save_and_validate_image(file, directory=COMPARE_DIR)
        rename_image(file=file, new=f"temp{count}")
        count += 1
    count = 1

    # O hash de cada imagem é extraido e é feito o calculo
    # para adquirir a porcentagem de similaridade
    first_hash = whash(Image.open(f"{COMPARE_DIR}temp1.jpeg"))
    second_hash = whash(Image.open(f"{COMPARE_DIR}temp2.jpeg"))
    size = len(first_hash)
    similarity = 100 - (((first_hash - second_hash) / size) * 100)

    # As imagens do diretório compare são removidas
    clear_compare()

    return {"resultados": f"As imagens são {similarity}% semelhantes"}


# Função de auxílio para salvar as imagens na aplicação e lidar
# com imagens que sejam corrompidas
def save_and_validate_image(file: UploadFile, directory: str):

    file_location = f"{directory}{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    try:
        img = Image.open(file_location)
        img.verify()
    except Exception:
        remove(file_location)
        clear_compare()
        raise HTTPException(status_code=400, detail="Arquivo corrompido")


# Função de auxílio para renomear imagens enviadas pelo usuário
def rename_image(file: UploadFile, new):

    old_name = f"{COMPARE_DIR}{file.filename}"
    new_name = f"{COMPARE_DIR}{new}.jpeg"

    rename(old_name, new_name)


# Função de auxílio para remover imagens salvas no diretório
# compare
def clear_compare():
    for filename in listdir(COMPARE_DIR):
        if filename.endswith(".jpeg"):
            remove(path.join(COMPARE_DIR, filename))
