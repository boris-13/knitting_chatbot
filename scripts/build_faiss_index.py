import json
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


def main() -> None:
    load_dotenv()

    faq_path = Path("data") / "knitting_faq.json"
    if not faq_path.exists():
        raise FileNotFoundError(f"FAQ file not found: {faq_path}")

    data = json.loads(faq_path.read_text(encoding="utf-8"))

    # Your JSON shape is {"faqs": [ ... ]} :contentReference[oaicite:19]{index=19}
    faqs = data.get("faqs", [])
    if not isinstance(faqs, list) or not faqs:
        raise ValueError("Expected non-empty list at data['faqs'].")

    docs = []
    for item in faqs:
        q = (item.get("question") or "").strip()
        a = (item.get("answer") or "").strip()
        cat = (item.get("category") or "").strip()

        if not q or not a:
            continue

        # Store both Q and A in content to improve retrieval
        content = f"Q: {q}\nA: {a}"
        docs.append(Document(page_content=content, metadata={"category": cat, "question": q}))

    if not docs:
        raise ValueError("No valid FAQ entries found to embed (empty questions/answers?).")

    embeddings = OpenAIEmbeddings()
    vs = FAISS.from_documents(docs, embeddings)
    vs.save_local("faiss_index")

    print(f"OK: built faiss_index with {len(docs)} documents.")


if __name__ == "__main__":
    main()
