import faiss
import numpy as np
import pickle
from typing import List, Dict


class FaissStore:
def __init__(self, dim=512, index_path=None):
self.dim = dim
self.index = faiss.IndexFlatL2(dim)
self.meta = [] # list of dicts aligned with vectors
self.index_path = index_path


def add(self, vectors: np.ndarray, metadata: List[Dict]):
if vectors.shape[1] != self.dim:
raise ValueError("Vectors dimension mismatch")
self.index.add(vectors)
self.meta.extend(metadata)


def search(self, vector: np.ndarray, k=5):
D, I = self.index.search(vector.reshape(1, -1), k)
results = []
for idx in I[0]:
if idx < len(self.meta):
results.append(self.meta[idx])
return results


def save(self):
if self.index_path:
faiss.write_index(self.index, self.index_path + ".idx")
with open(self.index_path + ".meta.pkl", "wb") as f:
pickle.dump(self.meta, f)


def load(self):
if self.index_path:
self.index = faiss.read_index(self.index_path + ".idx")
with open(self.index_path + ".meta.pkl", "rb") as f:
self.meta = pickle.load(f)