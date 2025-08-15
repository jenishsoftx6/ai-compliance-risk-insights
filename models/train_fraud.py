# train_fraud.py
import pandas as pd
from sklearn.ensemble import IsolationForest
from pathlib import Path

def train(input_csv: str, model_path: str = "models/artifacts/fraud_iforest.pkl"):
    from joblib import dump
    df = pd.read_csv(input_csv)
    features = ["amount","merchant_id","device_score","distance_from_last_km","foreign_txn","hour"]
    model = IsolationForest(contamination=0.02, random_state=123).fit(df[features])
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    dump(model, model_path)
    print(f"Saved: {model_path}")

if __name__ == "__main__":
    import sys
    train(sys.argv[1])
