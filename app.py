from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import json

from agents.analyzer_agent import AnalyzerAgent
from agents.explanation_agent import ExplanationAgent
import agents.clauses as cmod

from agents.rewrite_agent import RewriteAgent
from agents.scoring import score_document

rewrite_agent = RewriteAgent()

load_dotenv()

app = FastAPI()

analyzer = AnalyzerAgent()
explainer = ExplanationAgent()

class Document(BaseModel):
    text: str
    llm_fallback_for: list = None
    explain_clauses: bool = False

@app.post("/analyze")
def analyze(document: Document):
    return analyzer.analyze(document.text, llm_fallback_for=document.llm_fallback_for or [])

@app.post("/explain")
def explain(payload: dict):
    clause = payload.get("clause")
    text = payload.get("text", "")
    if not clause or not text:
        return {"error": "Provide 'clause' and 'text' in JSON body."}
    return explainer.explain_clause(clause, text)

@app.post("/analyze_and_explain")
def analyze_and_explain(document: Document):
    result_str = analyzer.analyze(document.text, llm_fallback_for=document.llm_fallback_for or [])
    
    # Parse JSON string to dictionary
    try:
        result = json.loads(result_str)
    except json.JSONDecodeError:
        return {"error": "Failed to parse analysis response", "raw": result_str}
    
    if document.explain_clauses:
        explanations = {}
        to_explain = result.get("missing_clauses", [])
        for clause, details in result.get("llm_checks", {}).items():
            if details.get("confidence", 100) < 60 and clause not in to_explain:
                to_explain.append(clause)
        for clause in to_explain:
            snippet_list = cmod.extract_relevant_sentences(document.text, clause, context_sentences=2)
            snippet = " ".join(snippet_list) if snippet_list else document.text[:2000]
            explanations[clause] = explainer.explain_clause(clause, snippet)
        result["explanations"] = explanations

    return result


# app.py additions


@app.post("/full_analysis")
def full_analysis(document: Document):
    # Step 1: Analyze
    result_str = analyzer.analyze(document.text, llm_fallback_for=document.llm_fallback_for or [])
    try:
        result = json.loads(result_str)
    except json.JSONDecodeError:
        return {"error": "Failed to parse analysis response", "raw": result_str}
    
    # Step 2: Explanations
    if document.explain_clauses:
        explanations = {}
        for clause in result.get("missing_clauses", []):
            snippet = " ".join(cmod.extract_relevant_sentences(document.text, clause, 2))
            explanations[clause] = explainer.explain_clause(clause, snippet)
        result["explanations"] = explanations

    # Step 3: Rewrite suggestions
    suggestions = {}
    for clause in result.get("missing_clauses", []) + [w.get("name") for w in result.get("weak_clauses", []) if isinstance(w, dict)]:
        suggestions[clause] = rewrite_agent.suggest_clause(clause)
    result["suggestions"] = suggestions

    # Step 4: Risk scoring
    result["risk_score"] = score_document(result)
    
    return result
