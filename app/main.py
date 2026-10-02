from pathlib import Path
from typing import List

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.agents.ingestion_agent import LogIngestionAgent
from app.agents.decision_agent import DecisionAgent


app = FastAPI(
    title="AI Log Anomaly Detection",
    description="API for intelligent anomaly detection in access logs",
    version="1.0.0"
)


# -----------------------------
# Modelos de entrada de la API
# -----------------------------

class AccessLog(BaseModel):
    method: str
    path: str
    status: int = Field(ge=100, le=599)
    response_time: float = Field(ge=0)


class AnalyzeRequest(BaseModel):
    logs: List[AccessLog]


# -----------------------------
# Cargar modelo de IA
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "model" / "anomaly_model.pkl"

if not MODEL_PATH.exists():
    raise RuntimeError(
        f"No se encontró el modelo entrenado en: {MODEL_PATH}"
    )

anomaly_model = joblib.load(MODEL_PATH)


# -----------------------------
# Inicializar agentes
# -----------------------------

ingestion_agent = LogIngestionAgent()
decision_agent = DecisionAgent()


# -----------------------------
# Endpoints
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "AI Log Anomaly Detection API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    try:
        # Convertir objetos Pydantic a diccionarios
        raw_logs = [
            log.model_dump()
            for log in request.logs
        ]

        # Agente 1: validar y normalizar logs
        processed_logs = ingestion_agent.process(raw_logs)

        # Modelo de IA: detectar anomalías
        predictions = anomaly_model.predict(processed_logs)

        # Agente 2: decidir acción
        decision = decision_agent.decide(predictions)

        return decision

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )