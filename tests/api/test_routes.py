from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_deidentify_endpoint():
    response = client.post(
        "/api/v1/deidentify",
        json={
            "text": "Marcus Whitfield lives in Boston."
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["masked_text"] != "Marcus Whitfield lives in Boston."
    assert "Marcus Whitfield" not in body["masked_text"]
    assert "Boston" not in body["masked_text"]

    assert body["mapping_id"]
    assert body["entities_detected"] == 2


def test_deidentify_rejects_empty_text():
    response = client.post(
        "/api/v1/deidentify",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422

def test_process_endpoint_protects_phi():
    response = client.post(
        "/api/v1/process",
        json={
            "text": "Marcus Whitfield lives in Boston."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["masked_text"] == (
        "Patient_001 lives in LOCATION_001."
    )

    assert data["llm_response"] == (
        "Clinical summary: "
        "Patient_001 lives in LOCATION_001."
    )

    assert data["final_response"] == (
        "Clinical summary: "
        "Marcus Whitfield lives in Boston."
    )

    assert data["mapping_id"]