
import uuid

import pytest
import requests

BASE_URL = "http://127.0.0.1:8003"


def crear_usuario():
    payload = {
        "nombre": "Usuario Original",
        "email": f"qa-{uuid.uuid4().hex}@test.com",
        "activo": True
    }

    response = requests.post(
        f"{BASE_URL}/usuarios",
        json=payload,
        timeout=10
    )

    assert response.status_code == 201
    return response.json()


def test_actualizar_usuario_exitosamente():
    usuario = crear_usuario()
    usuario_id = usuario["id"]

    datos_actualizados = {
        "nombre": "QA Automation Senior",
        "email": f"actualizado-{uuid.uuid4().hex}@test.com",
        "activo": False
    }

    response = requests.put(
        f"{BASE_URL}/usuarios/{usuario_id}",
        json=datos_actualizados,
        timeout=10
    )

    assert response.status_code == 200

    resultado = response.json()
    assert resultado["id"] == usuario_id
    assert resultado["nombre"] == datos_actualizados["nombre"]
    assert resultado["email"] == datos_actualizados["email"]
    assert resultado["activo"] is False

    # Verificar persistencia mediante GET
    consulta = requests.get(
        f"{BASE_URL}/usuarios/{usuario_id}",
        timeout=10
    )

    assert consulta.status_code == 200
    assert consulta.json()["nombre"] == "QA Automation Senior"
    assert consulta.json()["activo"] is False


def test_actualizar_usuario_inexistente():
    payload = {
        "nombre": "Usuario Inexistente",
        "email": f"inexistente-{uuid.uuid4().hex}@test.com",
        "activo": True
    }

    response = requests.put(
        f"{BASE_URL}/usuarios/999999999",
        json=payload,
        timeout=10
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


def test_actualizar_usuario_email_duplicado():
    usuario1 = crear_usuario()
    usuario2 = crear_usuario()

    payload = {
        "nombre": "Usuario Duplicado",
        "email": usuario1["email"],
        "activo": True
    }

    response = requests.put(
        f"{BASE_URL}/usuarios/{usuario2['id']}",
        json=payload,
        timeout=10
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "El email ya está registrado"


@pytest.mark.parametrize("email", [
    "correo-invalido",
    "sin-arroba.com",
    ""
])
def test_actualizar_usuario_email_invalido(email):
    usuario = crear_usuario()

    payload = {
        "nombre": "Usuario QA",
        "email": email,
        "activo": True
    }

    response = requests.put(
        f"{BASE_URL}/usuarios/{usuario['id']}",
        json=payload,
        timeout=10
    )

    assert response.status_code == 422
