import os
from functools import lru_cache
from typing import List, Dict, Any

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ---------- Paths & constants ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "policy_db")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ---------- Cached loaders (good for backend performance) ----------
@lru_cache(maxsize=1)
def _get_embeddings():
    print("[RAG] Loading embeddings model...")
    return HuggingFaceEmbeddings(model_name=MODEL_NAME)


@lru_cache(maxsize=1)
def _get_vectorstore():
    print("[RAG] Loading FAISS index from:", DB_PATH)
    embeddings = _get_embeddings()
    return FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


# ---------- Basic retrieval ----------
def retrieve_relevant_policies(query: str, k: int = 3):
    """
    Return top-k policy documents for a given query.
    Used when you just want context for the LLM.
    """
    vectorstore = _get_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)
    return docs


# ---------- Helper: format docs for LLM prompt ----------
def format_policies_for_prompt(docs) -> str:
    """
    Turn retrieved docs into a nice block of text
    that can be injected into your RAG prompt.
    """
    lines = []
    for i, doc in enumerate(docs, start=1):
        policy_name = doc.metadata.get("policy_name", f"policy_{i}")
        lines.append(
            f"{i}. [{policy_name}]\n{doc.page_content.strip()}"
        )
    return "\n\n".join(lines)


# ---------- Simple evaluation: matched / not matched ----------
def get_policy_matches(
    query: str,
    top_k: int = 5,
    score_threshold: float = 0.9,
) -> Dict[str, Any]:
    
    vectorstore = _get_vectorstore()
    docs_and_scores = vectorstore.similarity_search_with_score(
        query,
        k=top_k
    )

    matched = []
    not_matched = []

    for doc, score in docs_and_scores:
        policy_name = doc.metadata.get("policy_name", "unknown")
        item = {
            "policy_name": policy_name,
            "policy_text": doc.page_content,
            "score": float(score),
        }

        # HERE : LOWER SCORE = BETTER MATCH
        
        if score <= score_threshold:
            item["matched"] = True
            matched.append(item)
        else:
            item["matched"] = False
            not_matched.append(item)

    return {
        "query": query,
        "matched": matched,
        "not_matched": not_matched,
    }

# ---------- Main function for backend integration ----------
def analyze_document(contract_text: str) -> Dict[str, Any]:
    """
    This is the single function Person A will call from the backend.
    It analyzes the contract text and returns:
    - matched policies
    - not matched policies
    - scores
    """
    # We use your similarity-based matcher
    result = get_policy_matches(
        query=contract_text,
        top_k=5,
        score_threshold=0.9
    )

    return {
        "input_text": contract_text[:300] + "...",  # preview only
        "matched_policies": result["matched"],
        "not_matched_policies": result["not_matched"],
    }

# ---------- Quick manual tests ----------
if __name__ == "__main__":
    # Example 1: payment deadlines
    q1 = "This contract defines payment terms, due dates, and late fees clearly."
    res1 = get_policy_matches(q1, top_k=5)
    print("\n=== Test 1: Payment related query ===")
    print("Query:", res1["query"])
    print("\nMatched policies:")
    for m in res1["matched"]:
        print(" -", m["policy_name"], "(score:", m["score"], ")")

    # Example 2: confidentiality
    q2 = "Both parties must keep information confidential even after termination."
    res2 = get_policy_matches(q2, top_k=5)
    print("\n=== Test 2: Confidentiality query ===")
    print("Query:", res2["query"])
    print("\nMatched policies:")
    for m in res2["matched"]:
        print(" -", m["policy_name"], "(score:", m["score"], ")")
