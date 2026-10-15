
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import ScenarioConfig, NegotiationRequest
from negotiation_engine import run_negotiation

app = FastAPI(
    title="Multi-Agent Negotiation Simulator API",
    description="Scenario configuration and mock negotiation engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Multi-Agent Negotiation Simulator Backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "negotiation-backend",
    }


@app.post("/api/configure")
def configure_scenario(config: ScenarioConfig):
    return {
        "success": True,
        "message": "Scenario configuration received and validated.",
        "scenarioId": config.scenarioId,
        "scenarioName": config.scenarioName,
        "agentCount": len(config.agents),
        "agents": [
            {
                "id": agent.id,
                "name": agent.name,
                "role": agent.role,
                "personality": agent.personality,
            }
            for agent in config.agents
        ],
    }


@app.post("/api/negotiate")
def start_negotiation(request: NegotiationRequest):
    try:
        return run_negotiation(
            request.model_dump(),
            max_turns=request.maxTurns,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
