import pytest
from celery_app import calcular_soma, calcular_fatorial

def test_soma():
    assert calcular_soma(2, 5) == 7

def test_soma_negativo():
    assert calcular_soma(-2, -3) == -5

def test_fatorial():
    assert calcular_fatorial(5) == 120

def test_fatorial_zero():
    assert calcular_fatorial(0) == 1

def test_calcular_fatorial_numero_negativo_levanta_erro():
    with pytest.raises(ValueError):
        calcular_fatorial(-1)