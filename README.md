# Knitting Chatbot (Knibot) – FAQ RAG Backend

This repository contains a Flask-based API that answers knitting questions using Retrieval-Augmented Generation (RAG)
over a local FAISS vector index built from a JSON FAQ dataset.

## Project layout

- `app/chatbot_api.py` – Flask API (`POST /chat`)
- `data/knitting_faq.json` – FAQ dataset
- `scripts/build_faiss_index.py` – builds `faiss_index/` from the dataset
- `faiss_index/` – generated vector index (not committed)

## Prerequisites

- Python 3.10+
- An OpenAI API key

## Setup (local)

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
