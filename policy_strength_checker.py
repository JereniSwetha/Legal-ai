import re
from typing import Dict, Any

from rag_retrieve import get_policy_matches


# -------------------------------------------------------------------
# 1. KEYWORDS FOR EACH POLICY (simple rule engine)
# -------------------------------------------------------------------

POLICY_KEYWORDS = {
    "confidentiality": [
        "confidential", "confidentiality", "sensitive", "non-disclosure",
        "secret", "proprietary"
    ],
    "payment_deadline": [
        "payment", "pay", "due", "deadline", "invoice", "late fee",
        "interest", "overdue", "days"
    ],
    "termination_notice": [
        "terminate", "termination", "notice", "notice period",
        "cause", "convenience", "post-termination"
    ],
    "ip_ownership": [
        "intellectual property", "ip", "ownership", "license",
        "retain", "deliverables", "assign"
    ],
    "liability_limitations": [
        "liability", "limit", "cap", "damages", "indirect",
        "consequential", "aggregate", "fees"
    ],
    "governing_law": [
        "governing law", "jurisdiction", "courts", "state", "country",
        "venue"
    ],
    "dispute_resolution": [
        "dispute", "resolution", "mediation", "arbitration",
        "negotiation", "court", "escalation"
    ],
    "indemnity": [
        "indemnify", "indemnity", "hold harmless", "losses",
        "claims", "third party"
    ],
    "service_levels": [
        "service level", "sla", "uptime", "response time",
        "resolution time", "availability", "penalty"
    ],
    "data_protection": [
        "data", "protection", "privacy", "encryption",
        "access control", "retention", "personal data"
    ],
    "renewal_terms": [
        "renew", "renewal", "auto-renew", "renewal term",
        "expiry", "expiration", "notice"
    ],
    "warranties": [
        "warranty", "warranties", "guarantee", "defect",
        "performance", "quality"
    ],
    "audit_rights": [
        "audit", "inspect", "inspection", "records",
        "books", "access"
    ],
    "non_solicitation": [
        "non-solicit", "non solicitation", "solicit", "hire",
        "poach", "employees", "staff"
    ],
    "subcontracting": [
        "subcontract", "subcontractor", "delegate", "assignment",
        "assign", "approval", "responsible"
    ],
}


# -------------------------------------------------------------------
# 2. HELPER FUNCTIONS TO SCORE A CLAUSE
# -------------------------------------------------------------------

def _count_keyword_hits(text: str, keywords) -> int:
    """Count how many keywords appear in the text (case-insensitive)."""
    text_lower = text.lower()
    hits = 0
    for kw in keywords:
        if kw.lower() in text_lower:
            hits += 1
    return hits


def _has_numbers(text: str) -> bool:
    """Check if the clause mentions any numbers (e.g. 30 days, 12 months)."""
    return bool(re.search(r"\d", text))


def _has_time_words(text: str) -> bool:
    text_lower = text.lower()
    time_words = ["day", "days", "month", "months", "year", "years", "within"]
    return any(word in text_lower for word in time_words)


def score_clause_against_policy(
    clause_text: str,
    policy_name: str
) -> Dict[str, float]:
    """
    Rule-based scoring for:
      - completeness
      - compliance
      - clarity
    Returns scores out of 10.
    """
    clause = clause_text.strip()
    keywords = POLICY_KEYWORDS.get(policy_name, [])

    if not clause or not keywords:
        return {
            "completeness": 0.0,
            "compliance": 0.0,
            "clarity": 0.0,
        }

    # Completeness: how many important keywords are covered
    hits = _count_keyword_hits(clause, keywords)
    total = len(keywords)
    completeness = (hits / total) * 10.0
    completeness = round(min(completeness, 10.0), 1)

    # Compliance: for now, similar to completeness (could be more advanced)
    compliance = completeness

    # Clarity: boost if there are numbers or time words
    clarity = completeness
    if _has_numbers(clause):
        clarity += 2.0
    if _has_time_words(clause):
        clarity += 1.0
    clarity = round(min(clarity, 10.0), 1)

    return {
        "completeness": completeness,
        "compliance": compliance,
        "clarity": clarity,
    }


# -------------------------------------------------------------------
# 3. MAIN FUNCTION FOR DAY-3: ANALYZE CLAUSE STRENGTH
# -------------------------------------------------------------------

def analyze_clause_strength(
    clause_text: str,
    score_threshold: float = 1.3
) -> Dict[str, Any]:
    """
    High-level function for Day-3.

    Input: a contract clause (text)
    Output: information about:
      - which policy it relates to
      - scores (completeness, compliance, clarity)
      - is it strong / weak / missing
    """

    # 1. Use Day-2 RAG to find best-matching policy
    rag_result = get_policy_matches(
        clause_text,
        top_k=3,
        score_threshold=score_threshold,
    )

    matched = rag_result["matched"]

    if not matched:
        # Nothing matched strongly -> this looks like a missing policy
        return {
            "clause": clause_text,
            "status": "missing",
            "policy_name": None,
            "scores": {
                "completeness": 0.0,
                "compliance": 0.0,
                "clarity": 0.0,
            },
            "risk_score":100.0,
            "message": "No strong policy match found. This clause may be missing or too vague.",
        }

    # 2. Take the best match (first one)
    best = matched[0]
    policy_name = best["policy_name"]

    # 3. Compute rule-based scores
    scores = score_clause_against_policy(clause_text, policy_name)

    completeness = scores["completeness"]
    clarity = scores["clarity"]
    
        # 3b. Compute risk score (0–100)
    # Average of the three scores (0–10)
    avg_score = (
        scores["completeness"]
        + scores["compliance"]
        + scores["clarity"]
    ) / 3.0

    # Convert to risk: high score => low risk
    # Example: avg = 8 -> risk = 100 - 8*10 = 20
    risk_score = 100.0 - (avg_score * 10.0)
    # Keep it in [0, 100]
    risk_score = max(0.0, min(100.0, round(risk_score, 1)))

    # 4. Decide strong / weak based on scores
    if completeness >= 8.0 and clarity >= 8.0:
        status = "strong"
        msg = (
            f"The {policy_name} clause is present and looks strong. "
            f"It covers most important points with good detail."
        )
    elif completeness >= 4.0:
        status = "weak"
        msg = (
            f"The {policy_name} clause is present but appears weak or incomplete. "
            f"Consider adding more details to improve coverage and clarity."
        )
    else:
        status = "very_weak"
        msg = (
            f"The {policy_name} clause is present but very weak. "
            f"It likely misses several key elements."
        )

    return {
        "clause": clause_text,
        "status": status,
        "policy_name": policy_name,
        "scores": scores,
        "risk_score": risk_score,
        "message": msg,
    }


# -------------------------------------------------------------------
# 4. QUICK MANUAL TESTS
# -------------------------------------------------------------------

if __name__ == "__main__":
    test_clause_1 = """
    The client shall pay all invoices within 30 days of receipt.
    Late payments may incur interest on the overdue amount.
    """
    result1 = analyze_clause_strength(test_clause_1)
    print("\n=== Test: Payment Clause ===")
    print("Status:", result1["status"])
    print("Policy:", result1["policy_name"])
    print("Scores:", result1["scores"])
    print("Risk:", result1["risk_score"])
    print("Message:", result1["message"])

    test_clause_2 = """
    Both parties agree to keep all confidential information secret.
    """
    result2 = analyze_clause_strength(test_clause_2)
    print("\n=== Test: Confidentiality Clause ===")
    print("Status:", result2["status"])
    print("Policy:", result2["policy_name"])
    print("Scores:", result2["scores"])
    print("Risk:", result2["risk_score"])
    print("Message:", result2["message"])
