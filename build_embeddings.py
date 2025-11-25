import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Base paths (work even if you run from another folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICY_DIR = os.path.join(BASE_DIR, "policies")
DB_PATH = os.path.join(BASE_DIR, "policy_db")

def load_policy_texts():
    texts = []
    metadatas = []

    for file in sorted(os.listdir(POLICY_DIR)):
        if file.endswith(".txt"):
            full_path = os.path.join(POLICY_DIR, file)
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            policy_name = os.path.splitext(file)[0]  # e.g. confidentiality

            texts.append(content)
            metadatas.append({
                "policy_name": policy_name,
                "filename": file,
            })

    return texts, metadatas

def build_vectorstore():
    print("Loading policies from:", POLICY_DIR)
    texts, metadatas = load_policy_texts()

    print(f"Loaded {len(texts)} policies.")
    if not texts:
        raise ValueError("No .txt files found in policies/ folder!")

    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Building FAISS DB...")
    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    print("Saving DB to:", DB_PATH)
    vectorstore.save_local(DB_PATH)

    print("Embedding build complete ✔")

if __name__ == "__main__":
    build_vectorstore()
