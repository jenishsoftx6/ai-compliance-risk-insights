# 🛡️ AI-Powered Financial Compliance & Risk Insights

**One pane of glass** for risk leaders: real-time **fraud alerts**, **loan default risk**, and **compliance summaries** powered by AI.

> Built to showcase end-to-end skills across data, ML, LLMs, and product thinking — with banking-ready workflows.

---

## 🔎 What this does
- **Fraud** – Scores transactions using anomaly detection and flags top-risk events with reason codes.
- **Loans** – Predicts default risk and explains drivers (feature importance).
- **Compliance** – Summarizes regulatory text and highlights potential rule violations against recent activity.
- **Exec View** – KPI cards + drill-down tables; export to CSV/PDF.

---

## 🧱 Architecture
`Data → Models & NLP → App/API → Dashboard`

![Architecture](visuals/architecture.png)

---

## 🧰 Stack
- **Python**: pandas, scikit-learn, matplotlib, numpy
- **App**: Streamlit (demo UI)
- **Optional**: Azure ML / Azure OpenAI endpoints (placeholders included)
- **Packaging**: FastAPI (optional), Dockerfile (optional), Hugging Face/Streamlit Cloud (hosting)

---

## 🚀 Quickstart
```bash
# 1) Create venv and install
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) Launch the demo app
streamlit run app/app.py
```

**Sample data** lives in `data/raw`. If none is found, the app will generate synthetic demo data on the fly.

---

## 📈 Screenshots
*These are placeholders — replace with your real outputs as you progress.*

![Exec Overview](dashboards/screenshots/exec_overview.png)
![Fraud Workflow](visuals/fraud_workflow.png)
![Loan Feature Importance](visuals/loan_feature_importance.png)
![Compliance Flow](visuals/compliance_flow.png)

---

## 📂 Repo layout
```
ai-compliance-risk-insights/
├─ README.md
├─ requirements.txt
├─ app/
│  ├─ app.py
│  └─ components/
├─ models/
│  ├─ train_fraud.py
│  ├─ train_loan.py
│  └─ artifacts/
├─ nlp/
│  ├─ summarize_regulation.py
│  └─ prompts/aml_summary_prompt.txt
├─ data/
│  ├─ raw/
│  └─ processed/
├─ dashboards/
│  ├─ executive.pbix        # optional if you use Power BI
│  └─ screenshots/
├─ notebooks/
│  ├─ 01_fraud_eda.ipynb
│  └─ 02_loan_modeling.ipynb
├─ api/
│  └─ main.py               # optional FastAPI endpoint
├─ docker/
│  └─ Dockerfile
└─ visuals/
   ├─ architecture.png
   ├─ fraud_workflow.png
   ├─ loan_feature_importance.png
   └─ compliance_flow.png
```

---

## 🧪 What to measure (put in your README once you run models)
- **Fraud:** precision@k on top alerts, alert volume reduction
- **Loans:** ROC-AUC, confusion matrix, KS statistic
- **Compliance:** time saved (e.g., 200→2-page summaries), # flags matched to new guidance

---

## 🗺️ Roadmap
- Swap local models → Azure ML endpoints
- Add RBAC/auth & audit logging
- Add monitoring: drift, latency, cost
- Add CI/CD workflow and tests

---

**Author:** Bill Bell — IT Manager & Business Analyst (Banking) → AI Product/Solutions
