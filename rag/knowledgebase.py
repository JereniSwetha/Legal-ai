import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import hashlib

load_dotenv()

# Initialize Gemini Client (auto-loads GEMINI_API_KEY)
GEMINI_CLIENT = genai.Client()


class GeminiEmbeddings:

    def embed_documents(self, docs):
        """Embed multiple document chunks"""
        embeddings = []
        for text in docs:
            try:
                response = GEMINI_CLIENT.models.embed_content(
                    model="models/text-embedding-004",
                    content=text
                )
                embeddings.append(response.embedding.values)
            except Exception:
                embeddings.append(self._fallback_embedding(text))
        return embeddings

    def embed_query(self, query):
        """Embed user query"""
        try:
            response = GEMINI_CLIENT.models.embed_content(
                model="models/text-embedding-004",
                content=query
            )
            return response.embedding.values
        except Exception:
            return self._fallback_embedding(query)

    def _fallback_embedding(self, text, dim=768):
        """Deterministic fallback embeddings when Gemini API fails."""
        h = hashlib.sha256(text.encode('utf-8')).digest()
        vals = []
        cur = h
        while len(vals) < dim:
            cur = hashlib.sha256(cur).digest()
            vals.extend([b / 255.0 for b in cur])
        emb = vals[:dim]
        norm = sum(x * x for x in emb) ** 0.5
        return [x / norm for x in emb] if norm else emb


class KnowledgeBase:
    def __init__(self):
        self.embeddings = GeminiEmbeddings()
        self.db = None

    def build(self, texts):
        if not texts:
            raise ValueError("No documents provided to build the Knowledge Base")

        # Split documents
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.create_documents(texts)

        # Build vector DB
        self.db = Chroma.from_documents(
            chunks,
            embedding=self.embeddings
        )

    def query(self, question):
        if not self.db:
            raise ValueError("Knowledge base not built yet!")

        return self.db.similarity_search(question, k=3)
