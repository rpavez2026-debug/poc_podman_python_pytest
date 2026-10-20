import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"


def test_health_check():
    response = requests.get(f"{BASE_URL}/health", timeout=10)

    assert response.status_code == 200
    assert response.json()["status"] == "OK"


def test_consultar_usuario():
    response = requests.get(f"{BASE_URL}/usuarios/1", timeout=10)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["nombre"] == "Usuario QA"
    assert data["activo"] is True


@pytest.mark.parametrize("usuario_id", ["abc", "1.5", "null"])
def test_usuario_id_invalido(usuario_id):
    response = requests.get(
        f"{BASE_URL}/usuarios/{usuario_id}",
        timeout=10
    )

    assert response.status_code == 422


def test_endpoint_inexistente():
    response = requests.get(
        f"{BASE_URL}/endpoint-inexistente",
        timeout=10
    )

    assert response.status_code == 404