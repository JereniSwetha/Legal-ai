from rag.rag_agent import RAGAgent

# Initialize RAG agent
rag = RAGAgent(folder="./policies")

# Build knowledge base from documents
rag.build()

# Query KB
question = "What is the company's confidentiality policy?"
results = rag.query(question)

# Display results
for i, r in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(r.page_content)
    print()
