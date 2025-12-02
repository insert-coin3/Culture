import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

print(f"Key: {GOOGLE_API_KEY[:5]}...")

print("Listing models:")
try:
    for m in genai.list_models():
        print(f"- {m.name}")
        print(f"  Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing: {e}")

