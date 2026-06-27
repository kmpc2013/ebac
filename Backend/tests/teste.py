import pytest

def soma(a,b):
    return a+b


def test_soma_a():
    resultado = soma(2,3)
    assert resultado == 4

def test_soma_b():
    resultado = soma(2,3)
    assert resultado == 5