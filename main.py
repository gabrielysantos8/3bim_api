from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB
from schemas import ProdutoCreate, ProdutoResponse
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import FilmeDB
from schemas import FilmeCreate, FilmeResponse

Base.metadata.create_all(bind=engine) # cria as tabelas, se ainda não existirem
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # em produção, restringir para o domínio real do front-end
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()

@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

# GET /produtos/{id} -> retorna um único produto pelo id
@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto


# DELETE /produtos/{id} -> remove um produto do banco de dados
@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    db.delete(produto)
    db.commit()

# PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db:
Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade
    db.commit()
    db.refresh(produto)
    return produto


# Rotas filmes 

@app.get('/filmes', response_model=list[FilmeResponse])
def listar_filmes(db: Session = Depends(get_db)):
    return db.query(FilmeDB).all()

@app.get('/filmes/{filme_id}', response_model=FilmeResponse)
def obter_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = db.query(FilmeDB).filter(FilmeDB.id == filme_id).first()
    if filme is None:
        raise HTTPException(status_code=404, detail='Filme não encontrado')
    return filme

@app.post('/filmes', response_model=FilmeResponse, status_code=201)
def criar_filme(filme: FilmeCreate, db: Session = Depends(get_db)):
    novo_filme = FilmeDB(**filme.dict())
    db.add(novo_filme)
    db.commit()
    db.refresh(novo_filme)
    return novo_filme

@app.put('/filmes/{filme_id}', response_model=FilmeResponse)
def atualizar_filme(filme_id: int, dados: FilmeCreate, db:
Session = Depends(get_db)):
    filme = db.query(FilmeDB).filter(FilmeDB.id == filme_id).first()
    if filme is None:
        raise HTTPException(status_code=404, detail='Filme não encontrado')
    filme.titulo = dados.titulo
    filme.diretor = dados.diretor
    filme.genero = dados.genero
    filme.duracao_min = dados.duracao_min
    db.commit()
    db.refresh(filme)
    return filme

@app.delete('/filmes/{filme_id}', status_code=204)
def remover_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = db.query(FilmeDB).filter(FilmeDB.id == filme_id).first()
    if filme is None:
        raise HTTPException(status_code=404, detail='Filme não encontrado')
    db.delete(filme)
    db.commit()