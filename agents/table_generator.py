import os
from prettytable import PrettyTable

OUTPUT_DIR = "demo_outputs"
TABLE_DIR = os.path.join(OUTPUT_DIR, "tables")
os.makedirs(TABLE_DIR, exist_ok=True)

def generate_clause_table(analysis):
    """
    Generates a PrettyTable with columns: Clause | Issue | Risk | Explanation
    analysis: dict returned from AnalyzerAgent / analyze_and_explain
    """
    table = PrettyTable()
    table.field_names = ["Clause", "Issue", "Risk", "Explanation"]

    # Missing clauses
    for clause in analysis.get("missing_clauses", []):
        issue = "Missing"
        risk = "High"
        explanation = analysis.get("explanations", {}).get(clause, "")
        table.add_row([clause, issue, risk, explanation])

    # Weak clauses
    for clause in analysis.get("weak_clauses", []):
        issue = "Weak"
        risk = "Medium"
        explanation = analysis.get("explanations", {}).get(clause, "")
        table.add_row([clause, issue, risk, explanation])

    # Risky clauses (if any not already in missing/weak)
    for clause in analysis.get("risky_clauses", []):
        if clause not in analysis.get("missing_clauses", []) and clause not in analysis.get("weak_clauses", []):
            issue = "Risky"
            risk = "High"
            explanation = analysis.get("explanations", {}).get(clause, "")
            table.add_row([clause, issue, risk, explanation])

    return table

def save_table(analysis, filename="table_output.txt"):
    """Save the table as a text file in demo_outputs/tables"""
    table = generate_clause_table(analysis)
    filepath = os.path.join(TABLE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(table))
    return filepath

def process_multiple_documents(analyses):
    """
    analyses: list of analysis dictionaries
    Saves each table to demo_outputs/tables/
    """
    for i, analysis in enumerate(analyses, start=1):
        filename = f"document_{i}_table.txt"
        path = save_table(analysis, filename)
        print(f"[INFO] Table saved for Document {i}: {path}")
