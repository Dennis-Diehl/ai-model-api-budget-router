"""Schritt 8: FastAPI App - Alles zusammenfuehren.

Hier erstellst du die FastAPI-Anwendung mit drei Endpoints:
- GET  /health -> Health-Check
- POST /route  -> Prompt an den Router senden
- GET  /stats  -> Nutzungsstatistiken abrufen

Lernziele:
- FastAPI App erstellen und konfigurieren
- CORS Middleware (damit das Frontend zugreifen kann)
- GET und POST Endpoints definieren
- Request Validation mit Pydantic (passiert automatisch!)
- Error Handling mit HTTPException
- async/await fuer den LLM-Aufruf

Docs: https://fastapi.tiangolo.com/tutorial/first-steps/
Teste mit: uvicorn backend.app:app --reload -> dann http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.cost_estimator import calculate_actual_cost, estimate_cost, estimate_tokens
from backend.llm_client import call_llm
from backend.logging_service import get_stats, log_request
from backend.routing import select_model
from backend.schemas import HealthResponse, RouteRequest, RouteResponse, StatsResponse

# TODO: Erstelle die FastAPI App
# app = FastAPI(title="AI Model Budget Router")
app = FastAPI(title="AI Model Budget Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
   """Health-Check Endpoint.

   TODO:
   - Return ein HealthResponse Objekt mit status="ok"
   """
   pass


@app.post("/route", response_model=RouteResponse)
async def route(request: RouteRequest):
   """Haupt-Endpoint: Prompt routen und LLM-Antwort zurueckgeben.

   TODO:
   1. Modell auswaehlen mit select_model()
      - Fange ValueError ab -> HTTPException(status_code=400)
   2. Kosten vorab schaetzen:
      - input_tokens_est = estimate_tokens(request.prompt)
      - estimated_output = min(input_tokens_est * 2, 1024)
      - estimated_cost = estimate_cost(model_id, input_tokens_est, estimated_output)
   3. LLM aufrufen mit await call_llm(model_id, request.prompt)
      - Fange RuntimeError ab -> HTTPException(status_code=500)
      - Fange andere Exceptions ab -> HTTPException(status_code=502)
   4. Tatsaechliche Kosten berechnen mit calculate_actual_cost()
   5. Request loggen mit log_request()
   6. RouteResponse zurueckgeben mit allen Feldern
   """
   pass


@app.get("/stats", response_model=StatsResponse)
async def stats():
   """Statistik-Endpoint.

   TODO:
   - Hole Stats mit get_stats()
   - Return ein StatsResponse Objekt (Tipp: StatsResponse(**get_stats()))
   """
   pass
