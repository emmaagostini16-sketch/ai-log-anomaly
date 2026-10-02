from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_analyze_normal_logs():
    payload = {
        "logs": [
            {
                "method": "GET",
                "path": "/home",
                "status": 200,
                "response_time": 120
            },
            {
                "method": "GET",
                "path": "/products",
                "status": 200,
                "response_time": 150
            },
            {
                "method": "GET",
                "path": "/cart",
                "status": 200,
                "response_time": 110
            }
        ]
    }

    response = client.post(
        "/analyze",
        json=payload
    )

    data = response.json()

    assert response.status_code == 200
    assert data["threat_detected"] is False
    assert data["anomalies"] == 0
    assert data["action"] == "allow"


def test_analyze_suspicious_logs():
    payload = {
        "logs": [
            {
                "method": "GET",
                "path": "/home",
                "status": 200,
                "response_time": 120
            },
            {
                "method": "GET",
                "path": "/products",
                "status": 200,
                "response_time": 140
            },
            {
                "method": "GET",
                "path": "/cart",
                "status": 200,
                "response_time": 160
            },
            {
                "method": "GET",
                "path": "/etc/passwd",
                "status": 403,
                "response_time": 1800
            }
        ]
    }

    response = client.post(
        "/analyze",
        json=payload
    )

    data = response.json()

    assert response.status_code == 200
    assert data["threat_detected"] is True
    assert data["anomalies"] == 1
    assert data["action"] == "alert"


def test_analyze_high_risk_logs():
    payload = {
        "logs": [
            {
                "method": "PATCH",
                "path": "/api/unknown-resource",
                "status": 500,
                "response_time": 4500
            },
            {
                "method": "TRACE",
                "path": "/internal/debug",
                "status": 403,
                "response_time": 3200
            },
            {
                "method": "DELETE",
                "path": "/api/private/config",
                "status": 401,
                "response_time": 5100
            },
            {
                "method": "CONNECT",
                "path": "/internal/system",
                "status": 500,
                "response_time": 3900
            }
        ]
    }

    response = client.post(
        "/analyze",
        json=payload
    )

    data = response.json()

    assert response.status_code == 200
    assert data["threat_detected"] is True
    assert data["anomalies"] == 4
    assert data["action"] == "block"