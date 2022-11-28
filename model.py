from sqlalchemy import Column, Integer, String
from database import Base

# Criação de um modelo de tabelas e colunas no
# banco de dados


class Images(Base):

    __tablename__ = "images"
    id = Column(Integer, primary_key=True, autoincrement=True,
                index=True, nullable=False)
    image_name = Column(String(255), index=True, nullable=False)
