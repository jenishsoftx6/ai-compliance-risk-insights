# train_loan.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from joblib import dump
from pathlib import Path

def train(input_csv: str, model_path: str = "models/artifacts/loan_clf.pkl"):
    df = pd.read_csv(input_csv)
    X = df[["income","debt_to_income","credit_score","delinquencies","utilization","loan_amount"]]
    y = df["default"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    clf = LogisticRegression(max_iter=200).fit(X_train, y_train)
    auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:,1])
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    dump(clf, model_path)
    print(f"AUC: {auc:.3f} | Saved: {model_path}")

if __name__ == "__main__":
    import sys
    train(sys.argv[1])
