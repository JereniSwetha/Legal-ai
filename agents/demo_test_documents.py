# demo_test_documents.py
import os
import json
from agents.analyzer_agent import AnalyzerAgent
from agents.explanation_agent import ExplanationAgent
from agents.rewrite_agent import RewriteAgent
from agents.scoring import score_document
import agents.clauses as cmod
from agents.table_generator import generate_clause_table

# Create folders for outputs
OUTPUT_DIR = "demo_outputs"
TABLE_DIR = os.path.join(OUTPUT_DIR, "tables")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)

# Initialize agents
analyzer = AnalyzerAgent()
explainer = ExplanationAgent()
rewrite_agent = RewriteAgent()

# Sample documents for testing/demo
sample_docs = [
    {
        "name": "Missing termination & confidentiality",
        "text": "This agreement has no termination clause and no confidentiality obligations."
    },
    {
        "name": "Weak liability clause",
        "text": "The company may be liable for damages in certain circumstances."
    },
    {
        "name": "Complete contract",
        "text": """Termination: Either party may terminate with 30 days notice.
Confidentiality: All information must remain confidential.
Liability: Each party is responsible for their own actions.
Governing Law: This agreement is governed by the laws of California.
Payment: Fees will be paid within 30 days of invoice.
"""
    },
    {
        "name": "Force majeure missing",
        "text": "Neither party is responsible for delays due to unforeseen circumstances."
    },
]

def extract_context(text: str, clause_name: str, max_length: int = 2000) -> str:
    """Extract relevant context around a clause"""
    import re
    pattern = re.escape(clause_name)
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        start = max(0, match.start() - 500)
        end = min(len(text), match.end() + 500)
        return text[start:end]
    return text[:max_length]

def save_table_as_md(table, filename):
    """Save PrettyTable as markdown file"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(table.get_string())

def run_demo():
    for doc in sample_docs:
        print(f"\n=== Document: {doc['name']} ===\n")
        
        # Step 1: Analyze
        analysis_str = analyzer.analyze(doc["text"])
        try:
            analysis = json.loads(analysis_str)
        except json.JSONDecodeError:
            analysis = {"error": "Failed to parse analysis", "raw": analysis_str}
        
        # Step 2: Explanations
        explanations = {}
        for clause in analysis.get("missing_clauses", []):
            snippet_list = cmod.extract_relevant_sentences(doc["text"], clause, 2)
            snippet = " ".join(snippet_list) if snippet_list else doc["text"][:2000]
            explanations[clause] = explainer.explain_clause(clause, snippet)
        analysis["explanations"] = explanations

        # Step 3: Rewrite suggestions
        suggestions = {}
        missing_weak_clauses = analysis.get("missing_clauses", []) + \
                               [w.get("name") for w in analysis.get("weak_clauses", []) if isinstance(w, dict)]
        for clause in missing_weak_clauses:
            suggestions[clause] = rewrite_agent.suggest_clause(clause)
        analysis["suggestions"] = suggestions

        # Step 4: Risk scoring
        analysis["risk_score"] = score_document(analysis)

        # Step 5: Save JSON output
        json_file = os.path.join(OUTPUT_DIR, f"{doc['name'].replace(' ', '_')}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)
        
        # Step 6: Generate and save clause table
        table = generate_clause_table(analysis)
        table_file = os.path.join(TABLE_DIR, f"{doc['name'].replace(' ', '_')}.md")
        save_table_as_md(table, table_file)
        
        # Step 7: Print summary + table
        print(f"Missing Clauses: {analysis.get('missing_clauses', [])}")
        print(f"Weak Clauses: {analysis.get('weak_clauses', [])}")
        print(f"Risky Clauses: {analysis.get('risky_clauses', [])}")
        print(f"Top Risk Score: {analysis['risk_score']['total_score']}")
        print("\nClause Issue Table:")
        print(table)
        print(f"\nJSON Output: {json_file}")
        print(f"Markdown Table: {table_file}")

if __name__ == "__main__":
    run_demo()
