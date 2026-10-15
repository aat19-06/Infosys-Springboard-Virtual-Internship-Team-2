from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

Personality = Literal[
    "Aggressive",
    "Collaborative",
    "Risk-Averse",
]


class AgentConfig(BaseModel):
    id: str
    name: str
    role: str
    roleDescription: str
    goal: str
    constraints: list[str]
    personality: Personality

    @field_validator(
        "id",
        "name",
        "role",
        "roleDescription",
        "goal",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field must not be blank.")
        return value

    @field_validator("constraints")
    @classmethod
    def validate_constraints(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("At least one constraint is required.")

        if any(not constraint.strip() for constraint in value):
            raise ValueError("Constraints must not be blank.")

        return value


class ScenarioConfig(BaseModel):
    scenarioId: str
    scenarioName: str
    agents: list[AgentConfig] = Field(min_length=1)

    @field_validator("scenarioId", "scenarioName")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field must not be blank.")
        return value

    @model_validator(mode="after")
    def validate_unique_agent_ids(self) -> "ScenarioConfig":
        agent_ids = [agent.id for agent in self.agents]

        if len(agent_ids) != len(set(agent_ids)):
            raise ValueError("Agent IDs must be unique within a scenario.")

        return self


class NegotiationRequest(ScenarioConfig):
    maxTurns: int = Field(default=6, ge=1, le=20)
