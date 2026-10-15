
import pytest
from pydantic import ValidationError

from backend.schemas import ScenarioConfig


@pytest.fixture
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


def test_valid_scenario_config_is_accepted(valid_config):
    config = ScenarioConfig.model_validate(valid_config)
    assert config.scenarioId == "vendor-pricing"
    assert len(config.agents) == 2


@pytest.mark.parametrize(
    ("field", "value"),
    [("scenarioId", ""), ("scenarioName", "   ")],
)
def test_blank_scenario_fields_are_rejected(valid_config, field, value):
    valid_config[field] = value
    with pytest.raises(ValidationError):
        ScenarioConfig.model_validate(valid_config)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", "   "),
        ("name", ""),
        ("role", " "),
        ("roleDescription", "   "),
        ("goal", ""),
    ],
)
def test_blank_agent_fields_are_rejected(valid_config, field, value):
    valid_config["agents"][0][field] = value
    with pytest.raises(ValidationError):
        ScenarioConfig.model_validate(valid_config)


def test_duplicate_agent_ids_are_rejected(valid_config):
    valid_config["agents"][1]["id"] = "buyer"
    with pytest.raises(
        ValidationError, match="Agent IDs must be unique"
    ):
        ScenarioConfig.model_validate(valid_config)


@pytest.mark.parametrize("constraints", [[], [""], ["   "]])
def test_empty_or_blank_constraints_are_rejected(valid_config, constraints):
    valid_config["agents"][0]["constraints"] = constraints
    with pytest.raises(ValidationError):
        ScenarioConfig.model_validate(valid_config)


def test_invalid_personality_is_rejected(valid_config):
    valid_config["agents"][0]["personality"] = "Unknown"
    with pytest.raises(ValidationError):
        ScenarioConfig.model_validate(valid_config)


def test_empty_agent_list_is_rejected(valid_config):
    valid_config["agents"] = []
    with pytest.raises(ValidationError):
        ScenarioConfig.model_validate(valid_config)