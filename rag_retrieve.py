from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "policy_db"

def retrieve_relevant_policies(query):
    print("Loading embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Loading FAISS index...")
    vectorstore = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

    print("Searching...")
    docs = vectorstore.similarity_search(query, k=3)

    return docs

if __name__ == "__main__":
    result = retrieve_relevant_policies("payment deadline clause")
    for idx, doc in enumerate(result):
        print(f"\n--- Result {idx+1} ---")
        print(doc.page_content)
