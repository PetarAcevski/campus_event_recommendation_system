from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_students_endpoint_returns_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) == 80


def test_events_combined_filters():
    response = client.get(
        "/events",
        params={
            "category": "Technology",
            "free_only": "true",
        },
    )

    assert response.status_code == 200

    for event in response.json():
        assert event["category"] == "Technology"
        assert event["price"] == 0


def test_student_recommendations():
    response = client.get("/recommendations/1")

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == 1
    assert "student_name" in data
    assert "recommendations" in data

    if data["recommendations"]:
        recommendation = data["recommendations"][0]

        assert "score" in recommendation
        assert "distance_km" in recommendation
        assert "reason" in recommendation