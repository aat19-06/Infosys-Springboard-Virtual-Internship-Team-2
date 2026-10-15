
from typing import Literal

from pydantic import BaseModel, Field


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


class ScenarioConfig(BaseModel):
    scenarioId: str
    scenarioName: str
    agents: list[AgentConfig] = Field(min_length=1)


class NegotiationRequest(ScenarioConfig):
    maxTurns: int = Field(default=6, ge=1, le=20)
