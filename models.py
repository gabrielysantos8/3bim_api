from sqlalchemy import Column, Integer, String, Float
from database import Base
class ProdutoDB(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)

class FilmeDB(Base):
    __tablename__ = 'filmes'
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    diretor = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    duracao_min = Column(Integer, nullable=False)