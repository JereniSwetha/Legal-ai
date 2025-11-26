import re
from typing import Dict, List

CLAUSE_PATTERNS = {
    "termination": r"(termination|terminate|end the|expir|duration|term\s+of|notice period)",
    "confidentiality": r"(confidential|non.?disclosure|nda|secret|proprietary|trade\s+secret)",
    "liability": r"(liability|liable|indemnif|damages|compensation|hold harmless)",
    "governing_law": r"(governing\s+law|jurisdiction|court|legal\s+system|applicable\s+law)",
    "dispute_resolution": r"(arbitration|mediation|dispute|resolution|claim|litigation)",
    "payment": r"(payment|fee|cost|price|compensation|salary|invoice)",
    "intellectual_property": r"(intellectual\s+property|copyright|patent|trademark|ownership)",
    "warranty": r"(warrant|guarantee|representation|condition|merchantability)",
    "force_majeure": r"(force\s+majeure|act\s+of\s+god|unforeseen|extraordinary|impossible)",
    "limitation_of_liability": r"(limit.*liability|exclude.*liability|cap\s+liability)",
}

def find_clauses(text: str) -> Dict[str, bool]:
    """Find clauses using regex patterns"""
    found = {}
    text_lower = text.lower()
    
    for clause_type, pattern in CLAUSE_PATTERNS.items():
        found[clause_type] = bool(re.search(pattern, text_lower))
    
    return found

def extract_relevant_sentences(text: str, clause_name: str, context_sentences: int = 2) -> List[str]:
    """Extract sentences relevant to a clause"""
    sentences = re.split(r'[.!?]+', text)
    
    # Get pattern for this clause or use clause name as fallback
    clause_lower = clause_name.lower()
    pattern = CLAUSE_PATTERNS.get(clause_lower, re.escape(clause_name))
    
    relevant = []
    for i, sent in enumerate(sentences):
        if re.search(pattern, sent.lower()):
            start = max(0, i - context_sentences)
            end = min(len(sentences), i + context_sentences + 1)
            relevant.extend(sentences[start:end])
    
    return [s.strip() for s in relevant if s.strip()]

def get_clause_description(clause_name: str) -> str:
    """Get description of what a clause should contain"""
    descriptions = {
        "termination": "How and when the agreement can be ended",
        "confidentiality": "Protection of sensitive information and trade secrets",
        "liability": "Who is responsible for damages and how much",
        "governing_law": "Which jurisdiction's laws apply",
        "dispute_resolution": "How disagreements will be resolved",
        "payment": "Payment terms, amounts, and schedules",
        "intellectual_property": "Ownership of creations and innovations",
        "warranty": "Guarantees about the quality/condition of services",
        "force_majeure": "Protection from unforeseen circumstances",
        "limitation_of_liability": "Caps on financial responsibility",
    }
    return descriptions.get(clause_name.lower(), "Standard contract clause")