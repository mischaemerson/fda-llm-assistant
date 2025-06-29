# "Truth-Seeking" LLM Assistant for the FDA Drug Approval Process

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR-STREAMLIT-APP-URL.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.2-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--Turbo-purple.svg)

This project is a sophisticated, deployed AI assistant that answers questions about the FDA's drug approval process. It uses a Retrieval-Augmented Generation (RAG) pipeline to ensure every answer is based exclusively on a curated knowledge base of 12 official PDF documents, making it a reliable and trustworthy source of information.

## 🚀 Live Demo

You can try the live application here: **[https://YOUR-STREAMLIT-APP-URL.streamlit.app/](https://YOUR-STREAMLIT-APP-URL.streamlit.app/)**

## ✨ Key Features

* **Live & Interactive:** Deployed as a public web application using Streamlit Cloud.
* **Factual Grounding:** The RAG architecture prevents the LLM from hallucinating, forcing it to cite answers from the provided documents only.
* **Scalable Knowledge Base:** Ingests and processes multiple complex PDF documents, creating a single, searchable source of truth.
* **Efficient Retrieval:** Utilizes a FAISS vector database to perform rapid similarity searches.

## 🛠️ Tech Stack

* **Language:** Python
* **AI & ML:** LangChain, OpenAI, FAISS (Vector Store)
* **Web Framework & Deployment:** Streamlit, Streamlit Community Cloud
* **Data Processing:** PyMuPDF

## 🎓 Project Evolution & Key Learnings

This project was a journey through the entire development lifecycle, from local scripting to a fully deployed web application.

* **Initial Challenge:** A simple prototype failed when scaling to a large knowledge base, hitting the LLM's `context_length_exceeded` limit.
* **The Pivot:** This led to re-architecting the project into a full RAG pipeline using LangChain and FAISS to handle the large dataset efficiently.
* **The Deployment Gauntlet:** Deploying the app to Streamlit Cloud presented a new set of real-world challenges, including:
    * **API Secret Management:** Learning to use cloud-native secret management instead of local `.env` files.
    * **Dependency Conflicts:** Debugging multiple `ModuleNotFoundError` errors by creating a clean, precise `requirements.txt` file.
    * **Git Sync Issues:** Resolving `rejected push` and `bad object` errors by backing up local work and re-cloning from the remote source of truth.

This project taught me that building an AI model is only half the battle; deploying it, managing its environment, and debugging production-like issues are equally critical skills.

## 🚀 Local Installation

*(The local installation instructions remain the same)*