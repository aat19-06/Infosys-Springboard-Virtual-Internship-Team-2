
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Make the backend modules importable when pytest runs from the repo root.
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from main import app

client = TestClient(app)


def valid_config():
    return {
        "scenarioId": "vendor-pricing",
        "scenarioName": "Vendor Pricing",
        "agents": [
            {
                "id": "buyer",
                "name": "Buyer",
                "role": "Buyer",
                "roleDescription": "Purchases licenses",
                "goal": "Get a reasonable price",
                "constraints": ["Budget limit"],
                "personality": "Collaborative",
            },
            {
                "id": "vendor",
                "name": "Vendor",
                "role": "Vendor",
                "roleDescription": "Sells licenses",
                "goal": "Reach a profitable deal",
                "constraints": ["Minimum price"],
                "personality": "Aggressive",
            },
        ],
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_configure_accepts_valid_config():
    response = client.post("/api/configure", json=valid_config())

    assert response.status_code == 200


def test_configure_rejects_blank_scenario_name():
    payload = valid_config()
    payload["scenarioName"] = "   "

    response = client.post("/api/configure", json=payload)

    assert response.status_code == 422


def test_configure_rejects_duplicate_agent_ids():
    payload = valid_config()
    payload["agents"][1]["id"] = "buyer"

    response = client.post("/api/configure", json=payload)

    assert response.status_code == 422
