"""
Test dependencies individually.
"""
import sys
import time

print("Testing dependencies...")

print("Importing google.generativeai...", end=" ", flush=True)
try:
    import google.generativeai as genai
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")

print("Importing faiss...", end=" ", flush=True)
try:
    import faiss
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")

print("Importing numpy...", end=" ", flush=True)
try:
    import numpy as np
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")

print("Done.")
