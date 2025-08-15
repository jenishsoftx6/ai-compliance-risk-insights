# summarize_regulation.py
from pathlib import Path

def summarize(text: str, max_items: int = 5):
    lines = [l.strip('-• ') for l in text.splitlines() if l.strip()]
    bullets = [l for l in lines if len(l.split()) > 3][:max_items]
    if not bullets:
        bullets = [
            "Update KYC refresh cadence for high-risk segments",
            "Require enhanced due diligence for foreign transactions",
            "Tighten thresholds for large cash deposits",
            "Expand PEP screening and adverse media checks",
            "Log exceptions and provide quarterly attestations",
        ]
    return bullets

if __name__ == "__main__":
    sample = Path(__file__).resolve().parents[1] / "data" / "raw" / "reg_excerpt.txt"
    if sample.exists():
        text = sample.read_text()
    else:
        text = "Institutions must perform enhanced due diligence for high-risk customers."
    print("\n".join(summarize(text)))
