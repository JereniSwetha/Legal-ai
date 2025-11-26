from rag.loader import DocumentLoader
from rag.knowledgebase import KnowledgeBase

class RAGAgent:
    def __init__(self, folder="./policies"):
        self.loader = DocumentLoader(folder)
        self.kb = KnowledgeBase()

    def build(self):
        """Load all documents and build the knowledge base"""
        print("[INFO] Loading documents from:", self.loader.folder)
        docs = self.loader.load_documents()
        if not docs:
            print("[WARNING] No documents found!")
            return
        self.kb.build(docs)
        print(f"[INFO] Knowledge base built with {len(docs)} documents.")

    def query(self, question):
        """Search the KB for relevant chunks"""
        if not self.kb.db:
            print("[ERROR] Knowledge base not built yet!")
            return []
        results = self.kb.query(question)
        return results
