import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

POLICY_DIR = "policies"
DB_PATH = "policy_db"

def load_policy_texts():
    texts = []
    for file in os.listdir(POLICY_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(POLICY_DIR, file), "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts

def build_vectorstore():
    print("Loading policies...")
    texts = load_policy_texts()

    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Building FAISS DB...")
    vectorstore = FAISS.from_texts(texts, embeddings)

    print("Saving DB...")
    vectorstore.save_local(DB_PATH)

    print("Embedding build complete ✔")

if __name__ == "__main__":
    build_vectorstore()
