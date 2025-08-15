import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

st.set_page_config(page_title="Compliance & Risk Insights", layout="wide")

st.title("🛡️ AI-Powered Financial Compliance & Risk Insights")
st.caption("Demo: Fraud alerts • Loan risk scoring • Compliance summaries")

def load_or_generate_transactions(n=2000, seed=42):
    np.random.seed(seed)
    df = pd.DataFrame({
        "amount": np.random.exponential(scale=60, size=n),
        "merchant_id": np.random.randint(1, 200, size=n),
        "device_score": np.random.rand(n),
        "distance_from_last_km": np.abs(np.random.normal(loc=5, scale=10, size=n)),
        "foreign_txn": np.random.binomial(1, 0.05, size=n),
        "hour": np.random.randint(0, 24, size=n)
    })
    idx = np.random.choice(n, size=int(0.02*n), replace=False)
    df.loc[idx, "amount"] *= np.random.randint(10, 50, size=len(idx))
    df.loc[idx, "foreign_txn"] = 1
    return df

def load_or_generate_loans(n=2000, seed=7):
    np.random.seed(seed)
    df = pd.DataFrame({
        "income": np.random.normal(80000, 20000, n),
        "debt_to_income": np.clip(np.random.normal(0.28, 0.12, n), 0.01, 0.95),
        "credit_score": np.clip(np.random.normal(690, 60, n), 300, 850),
        "delinquencies": np.random.poisson(0.3, n),
        "utilization": np.clip(np.random.normal(0.4, 0.25, n), 0, 1),
        "loan_amount": np.random.normal(25000, 10000, n)
    })
    logit = (
        -8.0
        + 0.00002 * df["loan_amount"]
        + 2.8 * df["debt_to_income"]
        + 1.8 * df["utilization"]
        + 0.6 * df["delinquencies"]
        - 0.004 * df["credit_score"]
    )
    p = 1 / (1 + np.exp(-logit))
    df["default"] = np.random.binomial(1, p)
    return df

def summarize_regulation(text, max_items=5):
    lines = [l.strip("-• ") for l in text.splitlines() if l.strip()]
    bullets = [l for l in lines if len(l.split()) > 3][:max_items]
    if not bullets:
        bullets = ["Update KYC refresh cadence for high-risk segments",
                   "Require enhanced due diligence for foreign transactions",
                   "Tighten thresholds for large cash deposits",
                   "Expand PEP screening and adverse media checks",
                   "Log exceptions and provide quarterly attestations"]
    return bullets

def kpi_card(label, value):
    st.metric(label, value)

with st.sidebar:
    st.header("Data")
    tx_file = st.file_uploader("Upload Transactions CSV", type=["csv"], key="tx")
    loan_file = st.file_uploader("Upload Loans CSV", type=["csv"], key="loan")
    st.header("Compliance")
    reg_text = st.text_area("Paste a regulation excerpt (1–3 paragraphs):", height=200)

tab_exec, tab_fraud, tab_loans, tab_compliance = st.tabs(
    ["Executive Overview", "Fraud", "Loans", "Compliance"]
)

if tx_file:
    transactions = pd.read_csv(tx_file)
else:
    transactions = load_or_generate_transactions()

if loan_file:
    loans = pd.read_csv(loan_file)
else:
    loans = load_or_generate_loans()

with tab_fraud:
    st.subheader("Fraud Scoring")
    features = ["amount", "merchant_id", "device_score", "distance_from_last_km", "foreign_txn", "hour"]
    model = IsolationForest(contamination=0.02, random_state=123)
    scores = -model.fit_predict(transactions[features])
    risk = (scores - scores.min()) / (scores.max() - scores.min() + 1e-9) * 100
    transactions_scored = transactions.copy()
    transactions_scored["fraud_risk"] = risk.round(1)
    st.write("Top Alerts")
    topk = transactions_scored.sort_values("fraud_risk", ascending=False).head(20)
    st.dataframe(topk.reset_index(drop=True))
    st.download_button(
        "Download Flagged Alerts CSV",
        topk.to_csv(index=False).encode("utf-8"),
        file_name="flagged_alerts.csv",
        mime="text/csv"
    )

with tab_loans:
    st.subheader("Loan Default Risk")
    X = loans[["income","debt_to_income","credit_score","delinquencies","utilization","loan_amount"]]
    y = loans["default"]
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    clf = LogisticRegression(max_iter=200)
    clf.fit(X_train, y_train)
    proba = clf.predict_proba(X_test)[:,1]
    auc = roc_auc_score(y_test, proba)
    st.write(f"Test ROC-AUC: {auc:.3f}")
    pred = clf.predict_proba(X)[:,1]
    loans_scored = loans.copy()
    loans_scored["default_risk"] = (pred*100).round(1)
    st.write("Applicants (sample):")
    st.dataframe(loans_scored.head(25))
    import numpy as np
    coefs = pd.Series(clf.coef_[0], index=X.columns).sort_values(key=lambda s: np.abs(s), ascending=False)
    st.write("Feature Influence (abs coeff)")
    st.bar_chart(coefs.abs())
    st.download_button(
        "Download Scored Loans CSV",
        loans_scored.to_csv(index=False).encode("utf-8"),
        file_name="scored_loans.csv",
        mime="text/csv"
    )

with tab_compliance:
    st.subheader("Compliance Summary")
    default_text = (
        "Institutions must perform enhanced due diligence for high-risk customers. "
        "Cross-border transactions above defined thresholds require additional monitoring. "
        "Regular KYC refresh cycles must be maintained, with expedited reviews upon adverse media signals."
    )
    text = reg_text.strip() if reg_text else default_text
    bullets = summarize_regulation(text)
    st.write("Key Changes / Actions:")
    for b in bullets:
        st.write(f"- {b}")

with tab_exec:
    st.subheader("Executive KPIs (simulated)")
    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("Fraud Alerts Today", int((transactions_scored["fraud_risk"] > 90).sum()))
    with col2:
        kpi_card("High-Risk Loans (%)", f"{(loans_scored['default_risk']>60).mean()*100:.1f}%")
    with col3:
        kpi_card("Compliance Flags (7d)", 12)
    st.caption("KPIs are illustrative. Replace with your real thresholds/metrics as you iterate.")
