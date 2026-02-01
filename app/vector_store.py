import os
import pickle
import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension, cache_path=None):
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []
        self.cache_path = cache_path
        self.loaded_from_cache = False

        if cache_path and os.path.exists(cache_path):
            print("📦 Loading vector store from cache...")
            self._load()
            self.loaded_from_cache = True
        else:
            print("🆕 No cache found, creating new index...")

    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings))
        self.texts.extend(texts)

        if self.cache_path:
            print("💾 Saving vector store to cache...")
            self._save()

    def search(self, query_embedding, k=4):
        distances, indices = self.index.search(query_embedding, k)
        return [self.texts[i] for i in indices[0]]

    def _save(self):
        with open(self.cache_path, "wb") as f:
            pickle.dump((self.index, self.texts), f)

    def _load(self):
        with open(self.cache_path, "rb") as f:
            self.index, self.texts = pickle.load(f)
