
import uuid

import requests

BASE_URL = "http://127.0.0.1:8002"


def test_crear_usuario_exitosamente():
    email = f"qa-{uuid.uuid4().hex}@test.com"

    payload = {
        "nombre": "QA Automatizador",
        "email": email,
        "activo": True
    }

    response = requests.post(
        f"{BASE_URL}/usuarios",
        json=payload,
        timeout=10
    )

    assert response.status_code == 201

    usuario = response.json()

    assert isinstance(usuario["id"], int)
    assert usuario["nombre"] == payload["nombre"]
    assert usuario["email"] == email
    assert usuario["activo"] is True

    # Comprobar que el registro realmente se puede consultar
    consulta = requests.get(
        f"{BASE_URL}/usuarios/{usuario['id']}",
        timeout=10
    )

    assert consulta.status_code == 200
    assert consulta.json()["email"] == email


def test_crear_usuario_email_duplicado():
    email = f"duplicado-{uuid.uuid4().hex}@test.com"

    payload = {
        "nombre": "Usuario Duplicado",
        "email": email,
        "activo": True
    }

    primera = requests.post(
        f"{BASE_URL}/usuarios",
        json=payload,
        timeout=10
    )

    segunda = requests.post(
        f"{BASE_URL}/usuarios",
        json=payload,
        timeout=10
    )

    assert primera.status_code == 201
    assert segunda.status_code == 409
    assert segunda.json()["detail"] == "El email ya está registrado"


def test_crear_usuario_email_invalido():
    payload = {
        "nombre": "Usuario QA",
        "email": "correo-invalido",
        "activo": True
    }

    response = requests.post(
        f"{BASE_URL}/usuarios",
        json=payload,
        timeout=10
    )

    assert response.status_code == 422
