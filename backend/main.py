from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai_module import answer_question

app = FastAPI(title="Culture AI Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Culture AI Project is running."}

@app.get("/ask")
def ask(q: str):
    try:
        answer = answer_question(q)
        return {"question": q, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
