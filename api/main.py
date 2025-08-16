from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Risk Insights API", version="0.1.0")

class Txn(BaseModel):
    amount: float
    merchant_id: int
    device_score: float
    distance_from_last_km: float
    is_foreign: int
    hour: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/score/fraud")
def score_fraud(txn: Txn):
    risk = min(100.0, max(0.0, txn.amount/10 + 20*txn.is_foreign + (1-txn.device_score)*10))
    return {"fraud_risk": round(risk, 1)}
