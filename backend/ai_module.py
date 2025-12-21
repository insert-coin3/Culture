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

import time
import google.api_core.exceptions

async def answer_question(question: str):
    print(f"DEBUG: Current Env Keys: {list(os.environ.keys())}")
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"DEBUG: API Key loaded: {api_key[:5]}...")
    else:
        print("DEBUG: API Key is None")
    
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=api_key)
    
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
    
    max_retries = 5
    retry_delay = 20  # Seconds

    for attempt in range(max_retries):
        try:
            print(f"DEBUG: Attempt {attempt + 1} of {max_retries}...")
            response = await llm.ainvoke(prompt)
            print(f"DEBUG: Response Type: {type(response)}")
            print(f"DEBUG: Response Content Type: {type(response.content)}")
            print(f"DEBUG: Response Content: {response.content}")
            
            if isinstance(response.content, str):
                return response.content
            elif isinstance(response.content, list):
                # Handle list of blocks (e.g. [{'type': 'text', 'text': '...'}])
                texts = []
                for item in response.content:
                    if isinstance(item, dict) and 'text' in item:
                        texts.append(item['text'])
                    elif isinstance(item, str):
                        texts.append(item)
                    # Ignore non-text blocks to avoid pollution
                return "".join(texts)
            else:
                return str(response.content)

        except google.api_core.exceptions.ResourceExhausted as e:
            print(f"WARNING: Quota exceeded (Attempt {attempt + 1}). Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 1.5 # Exponential backoff
        except Exception as e:
            print(f"Error in answer_question: {e}")
            return "죄송합니다. 오류가 발생했습니다."
    
    return "죄송합니다. 사용량이 많아 답변을 생성하지 못했습니다. 잠시 후 다시 시도해주세요."
