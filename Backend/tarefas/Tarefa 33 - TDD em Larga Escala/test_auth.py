from fastapi.testclient import TestClient
from app import app
from dotenv import load_dotenv
import os
import pytest


client = TestClient(app)

load_dotenv()
MEU_USUARIO = "admin"
MINHA_SENHA = "admin"
AUTH_OK = (MEU_USUARIO, MINHA_SENHA)
AUTH_BAD_USER = ("user_error", MINHA_SENHA)
AUTH_BAD_PASS = (MEU_USUARIO, "password_error")


def post(endpoint, params=None, auth=AUTH_OK):
    kwargs = {}

    if params is not None:
        kwargs["params"] = params

    if auth is not None:
        kwargs["auth"] = auth

    return client.post(endpoint, **kwargs)

# ---------------------------------------------------------------------------
# Autenticação
# ---------------------------------------------------------------------------
def test_auth_user_with_success():
    response = client.get("/", auth=AUTH_OK)
    assert response.status_code == 200
    assert response.json()["Hello"] == "World!"

def test_auth_user_with_pass_error():
    response = client.get("/", auth=AUTH_BAD_PASS)
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"

def test_auth_user_with_user_error():
    response = client.get("/", auth=AUTH_BAD_USER)
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"

def test_auth_user_without_credentials():
    response = client.get("/")
    assert response.status_code == 401

# ---------------------------------------------------------------------------
# Endpoints - autenticação
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("endpoint", ["/soma", "/subtrair", "/dividir", "/multiplicar"])
def test_endpoint_without_credentials(endpoint):
    response = post(endpoint, params={"a": 1, "b": 1}, auth=None)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.parametrize("endpoint", ["/soma", "/subtrair", "/dividir", "/multiplicar"])
@pytest.mark.parametrize("auth", [AUTH_BAD_USER, AUTH_BAD_PASS])
def test_endpoint_with_invalid_credentials(endpoint, auth):
    response = post(endpoint, params={"a": 1, "b": 1}, auth=auth)
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"

# ---------------------------------------------------------------------------
# Endpoints - soma
# ---------------------------------------------------------------------------
def test_calc_sum_success():
    response = post("/soma", params={"a": 4, "b": 5})
    assert response.status_code == 200
    assert response.json() == 9

@pytest.mark.parametrize(
    "params",
    [
        {"a": 4, "b": "X"},
        {"a": "X", "b": 4},
        {"a": 4},
        {"b": 4},
    ],
)
def test_calc_sum_error_value_invalid(params):
    response = post("/soma", params=params)
    assert response.status_code == 400
    assert response.json()["detail"] == "Valores inválidos."

# ---------------------------------------------------------------------------
# Endpoints - subtrair
# ---------------------------------------------------------------------------
def test_calc_sub_success():
    response = post("/subtrair", params={"a": 10, "b": 5})
    assert response.status_code == 200
    assert response.json() == 5

@pytest.mark.parametrize(
    "params",
    [
        {"a": 10, "b": "X"},
        {"a": "X", "b": 10},
        {"a": 10},
        {"b": 10},
    ],
)
def test_calc_sub_error_value_invalid(params):
    response = post("/subtrair", params=params)
    assert response.status_code == 400
    assert response.json()["detail"] == "Valores inválidos."

# ---------------------------------------------------------------------------
# Endpoints - dividir
# ---------------------------------------------------------------------------
def test_calc_div_success():
    response = post("/dividir", params={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json() == 5.0

@pytest.mark.parametrize(
    "params",
    [
        {"a": 10, "b": 0},
        {"a": 10, "b": "X"},
        {"a": "X", "b": 2},
        {"a": 10},
        {"b": 2},
    ],
)
def test_calc_div_error_value_invalid(params):
    response = post("/dividir", params=params)
    assert response.status_code == 400
    assert response.json()["detail"] == "Valores inválidos."

# ---------------------------------------------------------------------------
# Endpoints - multiplicar
# ---------------------------------------------------------------------------
def test_calc_mult_success():
    response = post("/multiplicar", params={"a": 4, "b": 5})
    assert response.status_code == 200
    assert response.json() == 20

@pytest.mark.parametrize(
    "params",
    [
        {"a": 4, "b": "X"},
        {"a": "X", "b": 4},
        {"a": 4},
        {"b": 4},
    ],
)
def test_calc_mult_error_value_invalid(params):
    response = post("/multiplicar", params=params)
    assert response.status_code == 400
    assert response.json()["detail"] == "Valores inválidos."
