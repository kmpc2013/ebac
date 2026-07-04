from fastapi.testclient import TestClient
from main import app
import os
import pytest

client = TestClient(app)

os.environ["MEU_USUARIO"] = "admin"
os.environ["MINHA_SENHA"] = "admin"

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mock_redis_client = mocker.patch("main.redis_client", autospec=True)
    mock_redis_client.get.return_value = None

def test_auth_user_with_success():
    response = client.get (
        "/livros",
        auth=("admin", "admin")
    )
    assert response.status_code == 200

def test_auth_user_with_error():
    response = client.get(
        "/livros",
        auth=("usuario_incorreto", "admin")
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"

def test_auth_pass_with_error():
    response = client.get(
        "/livros",
        auth=("admin", "SENHA_INCORRETA")
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"
