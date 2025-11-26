from agents.table_generator import generate_clause_table, save_table
import json

analysis_json = """{
  "missing_clauses": ["termination", "confidentiality"],
  "weak_clauses": ["payment"],
  "risky_clauses": [],
  "explanations": {
    "termination": "Explanation text for termination...",
    "confidentiality": "Explanation text for confidentiality...",
    "payment": "Explanation text for payment..."
  }
}"""

analysis = json.loads(analysis_json)

# Generate table in console
table = generate_clause_table(analysis)
print(table)

# Save table to file
save_table(analysis, "test_doc_table.txt")
