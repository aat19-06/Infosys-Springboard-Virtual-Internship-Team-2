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


def test_negotiate_vendor_pricing_returns_result():
    payload = valid_config()
    payload["maxTurns"] = 6

    response = client.post("/api/negotiate", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert result["success"] is True
    assert result["scenarioId"] == "vendor-pricing"
    assert result["status"] in {"agreement", "no_agreement"}
    assert isinstance(result["transcript"], list)
    assert result["turnsUsed"] <= payload["maxTurns"]
    assert result["engine"] == "mock"


def test_negotiate_job_offer_returns_result():
    payload = valid_config()
    payload["scenarioId"] = "job-offer"
    payload["scenarioName"] = "Job Offer Negotiation"
    payload["maxTurns"] = 6

    payload["agents"] = [
        {
            "id": "candidate",
            "name": "Candidate",
            "role": "candidate",
            "roleDescription": "Negotiates employment terms.",
            "goal": "Obtain a suitable salary and benefits package.",
            "constraints": ["Stay within the acceptable salary range."],
            "personality": "Collaborative",
        },
        {
            "id": "recruiter",
            "name": "Recruiter",
            "role": "recruiter",
            "roleDescription": "Represents the hiring organization.",
            "goal": "Make a suitable offer within the hiring budget.",
            "constraints": ["Stay within the approved hiring budget."],
            "personality": "Collaborative",
        },
    ]

    response = client.post("/api/negotiate", json=payload)

    assert response.status_code == 200

    result = response.json()
    assert result["success"] is True
    assert result["scenarioId"] == "job-offer"
    assert isinstance(result["transcript"], list)


def test_negotiate_project_budget_returns_result():
    payload = valid_config()
    payload["scenarioId"] = "project-budget"
    payload["scenarioName"] = "Project Budget Allocation"
    payload["maxTurns"] = 6

    payload["agents"] = [
        {
            "id": "project-manager",
            "name": "Project Manager",
            "role": "project manager",
            "roleDescription": "Coordinates the project budget.",
            "goal": "Allocate funds to meet project priorities.",
            "constraints": ["Stay within the total project budget."],
            "personality": "Collaborative",
        },
        {
            "id": "department-lead",
            "name": "Department Lead",
            "role": "department lead",
            "roleDescription": "Represents the department's funding needs.",
            "goal": "Secure adequate funding for department priorities.",
            "constraints": ["Justify the requested allocation."],
            "personality": "Collaborative",
        },
    ]

    response = client.post("/api/negotiate", json=payload)

    assert response.status_code == 200

    result = response.json()
    assert result["success"] is True
    assert result["scenarioId"] == "project-budget"
    assert isinstance(result["transcript"], list)
