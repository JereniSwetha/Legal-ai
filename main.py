from agents.analyzer_agent import AnalyzerAgent
from agents.explanation_agent import ExplanationAgent
import json
import re

analyzer = AnalyzerAgent()
explainer = ExplanationAgent()

def process_legal_document(text):
    """Process a legal document and return analysis with explanations"""
    if not text or len(text.strip()) == 0:
        return {"error": "Document text cannot be empty"}
    
    # Analyze document
    analysis_str = analyzer.analyze(text)
    
    try:
        analysis = json.loads(analysis_str)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse analysis: {str(e)}", "raw": analysis_str}
    
    # Generate explanations for weak/missing clauses
    explanations = {}
    
    # Explain missing clauses
    for clause in analysis.get("missing_clauses", []):
        snippet = extract_context(text, clause, max_length=2000)
        explanations[clause] = explainer.explain_clause(clause, snippet)
    
    # Explain weak clauses if present
    for weak_clause in analysis.get("weak_clauses", []):
        clause_name = weak_clause.get("name") if isinstance(weak_clause, dict) else weak_clause
        snippet = extract_context(text, clause_name, max_length=2000)
        explanations[f"weak_{clause_name}"] = explainer.explain_clause(
            f"Why this is weak: {clause_name}", snippet
        )
    
    analysis["explanations"] = explanations
    return analysis

def extract_context(text: str, clause_name: str, max_length: int = 2000) -> str:
    """Extract relevant context around a clause"""
    pattern = re.escape(clause_name)
    
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        start = max(0, match.start() - 500)
        end = min(len(text), match.end() + 500)
        return text[start:end]
    
    return text[:max_length]

if __name__ == "__main__":
    # Test with sample document
    sample_doc = """This agreement has no termination clause and no confidentiality obligations."""
    result = process_legal_document(sample_doc)
    print(json.dumps(result, indent=2))