from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from vector_store import build_vector_store

vector_store = build_vector_store()
retriever = vector_store.as_retriever() if vector_store else None

def answer_question(question: str):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    if not retriever:
        return llm.invoke(question).content

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    result = qa_chain.run(question)
    return result
