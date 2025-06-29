# "Truth-Seeking" LLM Assistant for FDA Drug Approval

This project is a sophisticated AI assistant that uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions about the FDA’s drug approval process. It ensures factual accuracy by grounding all responses in a curated knowledge base of 12 official PDF documents.


# "Truth-Seeking" LLM Assistant for the FDA Drug Approval Process

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.2-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--Turbo-purple.svg)

This project is a sophisticated, command-line "truth-seeking" AI assistant specialized in the niche topic of the FDA's drug approval process. Unlike a general-purpose chatbot that can hallucinate or provide incorrect information, this assistant uses a Retrieval-Augmented Generation (RAG) pipeline to ensure every answer is based exclusively on a curated knowledge base of 12 official PDF documents. This project serves as a powerful demonstration of how to build reliable, factual, and specialized AI tools for complex domains.

## ✨ Key Features

* **Factual Grounding:** The RAG architecture prevents the LLM from using its general knowledge, forcing it to cite answers from the provided documents only. This makes the system trustworthy and verifiable.
* **Scalable Knowledge Base:** The system is designed to ingest and process multiple complex documents (PDFs), creating a single, searchable source of truth.
* **Efficient Retrieval:** Utilizes a FAISS vector database to perform rapid similarity searches, ensuring that only the most relevant information is retrieved to answer a user's query.
* **Modular Architecture:** Built with LangChain, the pipeline is modular, allowing for easy updates or swaps of components like the LLM, the document loaders, or the vector store.

## 🛠️ Tech Stack

* **Language:** Python
* **Core AI/ML Libraries:** LangChain, OpenAI
* **Vector Database:** FAISS (from Facebook AI) for in-memory vector storage
* **Data Processing:** PyMuPDF for PDF text extraction
* **Environment:** venv, pip, VS Code, Git

## ⚙️ How the RAG Pipeline Works

The assistant operates on a sophisticated Retrieval-Augmented Generation pipeline, which can be broken down into two phases:

1.  **Indexing (Done once at startup):**
    * **Load:** All 12 PDF documents from the `/data_pdfs` directory are loaded.
    * **Split:** The text from the documents is split into smaller, overlapping chunks to ensure semantic meaning is preserved.
    * **Embed:** Each chunk of text is converted into a numerical representation (an embedding) using OpenAI's embedding models.
    * **Store:** These embeddings are stored in a high-performance FAISS vector database in memory. This database allows for incredibly fast searching.

2.  **Retrieval and Generation (Done for every question):**
    * **Retrieve:** When a user asks a question, their query is also converted into an embedding. The FAISS database is then searched to find the text chunks with embeddings most similar to the question's embedding.
    * **Augment:** These relevant chunks of text are then "augmented" into a prompt that is sent to the OpenAI GPT-3.5-Turbo model.
    * **Generate:** The LLM generates a final answer based *only* on the context provided by the retrieved text chunks, ensuring the response is factual and grounded in the source documents.

## 🚀 Local Installation & Usage

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/mischaemerson/fda-llm-assistant.git](https://github.com/mischaemerson/fda-llm-assistant.git)
    cd fda-llm-assistant
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project folder and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your_secret_api_key_here"
    ```

5.  **Run the application:**
    ```bash
    python3 app_v3.py
    ```

## 🎓 Project Evolution & Key Learnings

This project was a journey through the practical challenges of building modern AI applications.

* **Initial Challenge:** My first attempt involved simply feeding all the text from the documents to the model in a single prompt. This immediately failed due to the **`context_length_exceeded` error**, a fundamental limitation of LLMs.
* **The Pivot:** This failure was the most important learning moment. It became clear that a more sophisticated architecture was needed. I pivoted to designing and implementing a full RAG pipeline.
* **The Solution:** By using LangChain to orchestrate the `Load -> Split -> Embed -> Retrieve` process, I was able to build a system that could handle a large knowledge base efficiently. Debugging this pipeline taught me invaluable lessons about API rate limits, library dependencies (`langchain-community`), and the importance of a well-structured project.

Ultimately, this project taught me that the difference between a simple AI toy and a professional AI tool is the architecture you build around the model to ensure reliability, scalability, and trustworthiness.

## 💡 Future Improvements

* **Web Interface:** Build a user-friendly web UI with Streamlit or Gradio to make the assistant accessible to non-technical users.
* **Source Citing:** Enhance the model to cite which document and page number the answer was retrieved from.
* **Automated Data Updates:** Implement a web scraper to periodically fetch new guidance documents from the FDA website to keep the knowledge base current.