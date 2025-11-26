import os

class DocumentLoader:
    def __init__(self, folder="./policies"):
        self.folder = folder

    def load_documents(self):
        docs = []
        for file in os.listdir(self.folder):
            if file.endswith(".txt"):
                with open(os.path.join(self.folder, file), "r", encoding="utf-8") as f:
                    docs.append(f.read())
        return docs
