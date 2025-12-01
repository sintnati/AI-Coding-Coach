try:
    import faiss
except ImportError:
    faiss = None

import numpy as np
import pickle
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class FaissStore:
    def __init__(self, dim=512, index_path=None):
        self.dim = dim
        self.index_path = index_path
        self.meta = [] # list of dicts aligned with vectors

        if faiss:
            self.index = faiss.IndexFlatL2(dim)
            self.use_faiss = True
        else:
            logger.warning("Faiss not available, using simple numpy fallback")
            self.index = []
            self.use_faiss = False

    def add(self, vectors: np.ndarray, metadata: List[Dict]):
        if vectors.shape[1] != self.dim:
            raise ValueError("Vectors dimension mismatch")

        if self.use_faiss:
            self.index.add(vectors)
        else:
            # Simple list append for fallback
            for v in vectors:
                self.index.append(v)

        self.meta.extend(metadata)

    def search(self, vector: np.ndarray, k=5):
        if self.use_faiss:
            D, I = self.index.search(vector.reshape(1, -1), k)
            results = []
            for idx in I[0]:
                if idx < len(self.meta) and idx >= 0:
                    results.append(self.meta[idx])
            return results
        else:
            # Simple linear search fallback
            if not self.index:
                return []

            # Calculate distances
            query = vector.reshape(1, -1)
            dists = []
            for i, v in enumerate(self.index):
                d = np.linalg.norm(v - query)
                dists.append((d, i))

            # Sort by distance
            dists.sort(key=lambda x: x[0])

            # Return top k
            results = []
            for _, idx in dists[:k]:
                if idx < len(self.meta):
                    results.append(self.meta[idx])
            return results

    def save(self):
        if self.index_path:
            if self.use_faiss:
                faiss.write_index(self.index, self.index_path + ".idx")
            with open(self.index_path + ".meta.pkl", "wb") as f:
                pickle.dump(self.meta, f)

    def load(self):
        if self.index_path:
            if self.use_faiss:
                try:
                    self.index = faiss.read_index(self.index_path + ".idx")
                except Exception as e:
                    logger.error(f"Failed to load faiss index: {e}")

            try:
                with open(self.index_path + ".meta.pkl", "rb") as f:
                    self.meta = pickle.load(f)
            except Exception as e:
                logger.error(f"Failed to load metadata: {e}")
