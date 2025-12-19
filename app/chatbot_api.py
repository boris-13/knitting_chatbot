import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    # Lazy-init so startup errors are clearer
    embedding = OpenAIEmbeddings()

    if not os.path.isdir("faiss_index"):
        raise RuntimeError(
            "Missing faiss_index/. Build it first:\n"
            "  python scripts/build_faiss_index.py\n"
            "Then rerun the API."
        )

    db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model_name)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )

    @app.get("/")
    def root():
        return "<p>Knitting FAQ chatbot backend is running.</p>"

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/chat")
    def chat():
        data = request.get_json(silent=True) or {}
        question = (data.get("question") or "").strip()
        if not question:
            return jsonify({"error": "Missing question"}), 400

        answer = qa_chain.run(question)
        return jsonify({"answer": answer})

    return app


app = create_app()
