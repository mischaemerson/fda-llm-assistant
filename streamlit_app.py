import streamlit as st
import os
from dotenv import load_dotenv

# --- All your existing LangChain imports ---
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# --- Page Configuration (New for Streamlit) ---
st.set_page_config(
    page_title="FDA 'Truth-Seeking' Assistant",
    page_icon="💊",
    layout="wide"
)

# --- Caching the RAG Pipeline (CRITICAL FOR PERFORMANCE) ---
# This decorator tells Streamlit to run this function only once and cache the result.
# This prevents reloading and re-indexing all the PDFs every time a user asks a question.
@st.cache_resource
def setup_rag_pipeline(directory_path):
    """
    This function builds the entire RAG pipeline.
    It loads PDFs, splits them into chunks, creates embeddings,
    and sets up the retriever.
    """
    # The setup logic is the same as your app_v3.py
    # We just add st.spinner to show a loading message.
    with st.spinner("Indexing knowledge base... This may take a moment."):
        all_docs = []
        for filename in os.listdir(directory_path):
            if filename.endswith(".pdf"):
                filepath = os.path.join(directory_path, filename)
                loader = PyMuPDFLoader(filepath)
                docs = loader.load()
                all_docs.extend(docs)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(all_docs)

        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(split_docs, embeddings)
        retriever = vector_store.as_retriever()
    
    return retriever

def main():
    """Main function to run the Streamlit web app."""
    # Load environment variables
    load_dotenv()

    # --- UI Elements (New for Streamlit) ---
    st.title("💊 'Truth-Seeking' AI Assistant for FDA Drug Approval")
    st.markdown("""
    Welcome! This AI assistant is designed to answer questions about the FDA's drug approval process. 
    It uses a Retrieval-Augmented Generation (RAG) pipeline, which means it bases its answers *only* on a knowledge base of 12 official FDA documents. 
    Ask a question below to get a factual, verifiable answer.
    """)

    # Setup the pipeline (this will be cached)
    try:
        retriever = setup_rag_pipeline("data_pdfs")
    except Exception as e:
        st.error(f"Failed to load the knowledge base. Error: {e}")
        st.stop()

    # Define the LLM and the prompt template
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant for the FDA drug approval process.
    Answer the user's question based only on the following context:

    <context>
    {context}
    </context>
    
    If you don't know the answer from the context provided, just say that you cannot find the answer in the provided documents.

    Question: {input}
    """)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # --- User Input and Response (New for Streamlit) ---
    # We use st.text_input instead of input()
    user_question = st.text_input("Ask your question here:")

    # If the user has entered a question, run the chain
    if user_question:
        with st.spinner("Searching documents and generating answer..."):
            response = retrieval_chain.invoke({"input": user_question})
            st.write(response["answer"])

if __name__ == "__main__":
    main()