import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool  # ← Adicione este import
from main import Base, LivroDB, app, sessao_db  # ← Importe sessao_db
from fastapi.testclient import TestClient
import os


DATABASE_URL_TEST = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ← Adicione esta linha
)
TestingSessionLocal = sessionmaker(bind=engine)

# ✨ Criar tabelas no engine de teste
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mock_redis_client = mocker.patch("main.redis_client", autospec=True)
    mock_redis_client.get.return_value = None

@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        # Inserir dados de teste
        livro = LivroDB(
            nome_livro="Livro A",
            autor_livro="Autor 01",
            ano_livro=1994
        )
        db.add(livro)
        db.commit()
        
        # ✨ Override: faz o endpoint usar o banco de teste
        app.dependency_overrides[sessao_db] = lambda: db
        
        yield db
    finally:
        # Limpar override após teste
        app.dependency_overrides.clear()
        db.close()

def test_get_books(db):
    response = client.get("/livros", auth=("admin", "admin"))
    assert response.status_code == 200
    
    data = response.json()
    
    assert len(data["livros"]) > 0
    assert data["livros"][0]["nome_livro"] == "Livro A"
    assert data["livros"][0]["autor_livro"] == "Autor 01"
    assert data["livros"][0]["ano_livro"] == 1994