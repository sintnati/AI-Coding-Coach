import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"Testing API Key: {api_key[:10]}...{api_key[-5:]}")

try:
    genai.configure(api_key=api_key)
    # Use a newer available model
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Hello, are you working?")
    print("SUCCESS: API Key is valid!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"ERROR: API Key check failed: {e}")
