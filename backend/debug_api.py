import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Testing with API Key: {api_key[:5]}...{api_key[-5:]}")

# 1. Test Direct Generation with genai (bypassing langchain for a moment to list models)
genai.configure(api_key=api_key)
print("\n--- Available Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")

# 2. Test LangChain Integration with gemini-2.0-flash
print("\n--- Testing LangChain with gemini-2.0-flash ---")
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
    response = llm.invoke("Hello, are you working?")
    print(f"Response: {response.content}")
except Exception as e:
    print(f"Error with gemini-2.0-flash: {e}")

# 3. Test LangChain Integration with gemini-1.5-flash (fallback)
print("\n--- Testing LangChain with gemini-1.5-flash ---")
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    response = llm.invoke("Hello, are you working?")
    print(f"Response: {response.content}")
except Exception as e:
    print(f"Error with gemini-1.5-flash: {e}")
