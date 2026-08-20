from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    quantidade: int

class ProdutoCreate(ProdutoBase):
    pass
    
class ProdutoResponse(ProdutoBase):
    id: int

class Config:
    from_attributes = True

class FilmeBase(BaseModel):
    titulo: str
    diretor: str
    genero: str
    duracao_min: int

class FilmeCreate(FilmeBase):
    pass
    
class FilmeResponse(FilmeBase):
    id: int
