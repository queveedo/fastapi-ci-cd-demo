from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_responde_correctamente() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_endpoint_doble_calcula_resultado() -> None:
    response = client.get("/doble/7")

    assert response.status_code == 200
    assert response.json() == {"numero": 7.0, "resultado": 14.0}


def test_endpoint_doble_rechaza_texto() -> None:
    response = client.get("/doble/hola")

    assert response.status_code == 422
