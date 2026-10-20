
import pytest
import requests

BASE_URL = "http://127.0.0.1:8001"


def test_consultar_usuario_existente():
    response = requests.get(
        f"{BASE_URL}/usuarios/1",
        timeout=10
    )

    assert response.status_code == 200

    usuario = response.json()

    assert usuario["id"] == 1
    assert usuario["nombre"] == "Usuario QA"
    assert usuario["email"] == "qa@test.com"
    assert usuario["activo"] is True


def test_consultar_usuario_inexistente():
    response = requests.get(
        f"{BASE_URL}/usuarios/999999",
        timeout=10
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


@pytest.mark.parametrize(
    "usuario_id",
    ["abc", "1.5", "null"]
)
def test_consultar_usuario_id_invalido(usuario_id):
    response = requests.get(
        f"{BASE_URL}/usuarios/{usuario_id}",
        timeout=10
    )

    assert response.status_code == 422
