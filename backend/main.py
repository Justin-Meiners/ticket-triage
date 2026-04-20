from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import triage

app = FastAPI(title="Ticket Triage API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
