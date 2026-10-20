
import uuid

import requests

BASE_URL = "http://127.0.0.1:8004"


def test_crud_completo_usuario():
    email = f"e2e-{uuid.uuid4().hex}@test.com"

    # 1. CREATE
    payload = {
        "nombre": "Usuario E2E",
        "email": email,
        "activo": True
    }

    response = requests.post(
        f"{BASE_URL}/usuarios",
        json=payload,
        timeout=10
    )

    assert response.status_code == 201
    usuario_id = response.json()["id"]

    try:
        # 2. READ
        response = requests.get(
            f"{BASE_URL}/usuarios/{usuario_id}",
            timeout=10
        )

        assert response.status_code == 200
        assert response.json()["nombre"] == "Usuario E2E"

        # 3. UPDATE
        datos_actualizados = {
            "nombre": "Usuario E2E Actualizado",
            "email": email,
            "activo": False
        }

        response = requests.put(
            f"{BASE_URL}/usuarios/{usuario_id}",
            json=datos_actualizados,
            timeout=10
        )

        assert response.status_code == 200
        assert response.json()["activo"] is False

        # 4. READ después de UPDATE
        response = requests.get(
            f"{BASE_URL}/usuarios/{usuario_id}",
            timeout=10
        )

        assert response.status_code == 200
        assert response.json()["nombre"] == "Usuario E2E Actualizado"
        assert response.json()["activo"] is False

    finally:
        # 5. DELETE, incluso si falla una validación anterior
        response = requests.delete(
            f"{BASE_URL}/usuarios/{usuario_id}",
            timeout=10
        )

    # 6. READ después de DELETE
    assert response.status_code == 204

    response = requests.get(
        f"{BASE_URL}/usuarios/{usuario_id}",
        timeout=10
    )

    assert response.status_code == 404
