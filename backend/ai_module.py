from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from vector_store import build_vector_store

vector_store = build_vector_store()
retriever = vector_store.as_retriever() if vector_store else None

def answer_question(question: str):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    try:
        if not retriever:
            return llm.invoke(question).content

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )
        result = qa_chain.run(question)
        return result
    except Exception as e:
        print(f"Error in answer_question: {e}")
        return "죄송합니다. 현재 AI 서비스 사용량이 많아 답변을 드릴 수 없습니다. (Quota Exceeded or Error)"
