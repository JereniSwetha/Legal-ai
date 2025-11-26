# agents/scoring.py

def score_document(analysis: dict) -> dict:
    """
    Assign risk score based on missing/weak/risky clauses.
    Missing clause = 5 points, weak clause = 3, risky clause = 7.
    """
    score = 0
    score += 5 * len(analysis.get("missing_clauses", []))
    score += 3 * len(analysis.get("weak_clauses", []))
    score += 7 * len(analysis.get("risky_clauses", []))
    
    return {
        "total_score": score,
        "missing_clauses": len(analysis.get("missing_clauses", [])),
        "weak_clauses": len(analysis.get("weak_clauses", [])),
        "risky_clauses": len(analysis.get("risky_clauses", []))
    }
