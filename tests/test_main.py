import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_pagina_principal(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200


def test_pagina_principal_devuelve_html(client):
    respuesta = client.get("/")
    assert b"<html" in respuesta.data.lower()