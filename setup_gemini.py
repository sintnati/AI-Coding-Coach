"""
Simple script to help set up your .env file with Gemini API key.
Run this to create your .env file interactively.
"""
import os

print("=" * 60)
print("Gemini API Setup for AI Coding Coach")
print("=" * 60)
print()

# Check if .env already exists
env_path = ".env"
if os.path.exists(env_path):
    print("⚠️  .env file already exists!")
    overwrite = input("Do you want to overwrite it? (y/n): ").lower()
    if overwrite != 'y':
        print("Setup cancelled.")
        exit(0)

print("Step 1: Get your Gemini API key")
print("  → Visit: https://aistudio.google.com/app/apikey")
print("  → Click 'Create API Key'")
print("  → Copy your API key")
print()

api_key = input("Paste your Gemini API key here: ").strip()

if not api_key:
    print("❌ No API key provided. Setup cancelled.")
    exit(1)

if not api_key.startswith("AIzaSy"):
    print("⚠️  Warning: API key doesn't look like a Gemini key (should start with 'AIzaSy')")
    proceed = input("Continue anyway? (y/n): ").lower()
    if proceed != 'y':
        print("Setup cancelled.")
        exit(1)

print()
print("Step 2: Choose Gemini model (optional)")
print("  1. gemini-2.0-flash-exp (Recommended - Fast & Smart)")
print("  2. gemini-1.5-flash (Fast & Cheap)")
print("  3. gemini-1.5-pro (Powerful but slower)")
print()

model_choice = input("Enter choice (1-3) or press Enter for default [1]: ").strip()

models = {
    "1": "gemini-2.0-flash-exp",
    "2": "gemini-1.5-flash",
    "3": "gemini-1.5-pro",
    "": "gemini-2.0-flash-exp"
}

model = models.get(model_choice, "gemini-2.0-flash-exp")

# Create .env file
env_content = f"""# Gemini API Configuration
# Get your API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY={api_key}

# Gemini model to use
GEMINI_MODEL={model}
"""

with open(env_path, "w") as f:
    f.write(env_content)

print()
print("=" * 60)
print("✅ Success! .env file created")
print("=" * 60)
print()
print("Your configuration:")
print(f"  API Key: {api_key[:20]}...{api_key[-4:]}")
print(f"  Model: {model}")
print()
print("Next steps:")
print("  1. Run: python services/gateway/app.py")
print("  2. Open: http://localhost:8080")
print("  3. Enter your coding platform usernames")
print("  4. Get AI analysis!")
print()
print("Note: The system will automatically use Gemini to fetch")
print("      profile data when platform APIs fail.")
print()
