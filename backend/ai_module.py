from langchain_google_genai import ChatGoogleGenerativeAI

from public_data import fetch_public_data

# Vector store disabled due to quota limits
# vector_store = build_vector_store()
# retriever = vector_store.as_retriever() if vector_store else None

import os
from dotenv import load_dotenv
import pathlib

env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

async def answer_question(question: str):
    print(f"DEBUG: Current Env Keys: {list(os.environ.keys())}")
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"DEBUG: API Key loaded: {api_key[:5]}...")
    else:
        print("DEBUG: API Key is None")
    
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=api_key)
    try:
        # Fetch live culture data
        culture_data = fetch_public_data()
        context = "\n".join(culture_data) if culture_data else "No culture data available."

        # Construct prompt with context
        prompt = f"""You are a helpful assistant for the Culture AI Project.
Use the following context about current cultural events to answer the user's question.
If the answer is not in the context, answer based on your general knowledge but mention that you don't have specific info on that.

Context (Current Cultural Events):
{context}

User Question: {question}
"""
        
        response = await llm.ainvoke(prompt)
        return response.content

    except Exception as e:
        print(f"Error in answer_question: {e}")
        return "죄송합니다. 오류가 발생했습니다."
