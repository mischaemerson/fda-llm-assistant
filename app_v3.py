import os
from dotenv import load_dotenv

# --- New LangChain Imports ---
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate


def setup_rag_pipeline(directory_path):
    """
    This function builds the entire RAG pipeline.
    It loads PDFs, splits them into chunks, creates embeddings,
    and sets up the retriever.
    """
    print("Setting up the RAG pipeline...")
    
    # 1. Load all PDF documents from the specified directory
    all_docs = []
    print("Loading documents...")
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory_path, filename)
            loader = PyMuPDFLoader(filepath)
            docs = loader.load()
            all_docs.extend(docs)
            print(f"  - Loaded {filename}")

    # 2. Split the loaded documents into smaller chunks for processing
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(all_docs)

    # 3. Create embeddings (numerical representations) for each chunk
    # This allows us to do similarity searches
    print("Creating embeddings and building vector store...")
    embeddings = OpenAIEmbeddings()

    # 4. Create the FAISS vector store (our searchable database)
    # This will take a moment as it processes all the document chunks
    vector_store = FAISS.from_documents(split_docs, embeddings)
    
    # 5. Create the retriever, which finds relevant chunks based on a query
    retriever = vector_store.as_retriever()
    print("RAG pipeline setup complete!")
    
    return retriever


def main():
    """Main function to run the RAG-powered assistant."""
    # Load the OpenAI API key from the .env file
    load_dotenv()
    
    # This only needs to be done once when the app starts
    retriever = setup_rag_pipeline("data_pdfs")

    # Define the LLM we want to use
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # Create a prompt template. This tells the AI how to behave.
    # The 'context' is where we will put the relevant paragraphs we find.
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant for the FDA drug approval process.
    Answer the user's question based only on the following context:

    <context>
    {context}
    </context>
    
    If you don't know the answer from the context provided, just say that you cannot find the answer in the provided documents.

    Question: {input}
    """)

    # This chain will combine the prompt and the LLM
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    # This is the final chain that takes a question, uses the retriever
    # to find relevant documents, and passes them to the document_chain.
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    print("\n--- Welcome to the RAG-Powered FDA Drug Approval Assistant! ---")
    print("My knowledge comes from the PDF documents you provided.")
    print("Ask a question (or type 'quit' to exit).")
    
    while True:
        user_question = input("\nYour question: ")
        if user_question.lower() == 'quit':
            break
        
        # Use the retrieval chain to get an answer
        # The chain handles finding relevant docs and generating the response
        response = retrieval_chain.invoke({"input": user_question})
        
        # Print the answer neatly
        print("\nAssistant:")
        print(response["answer"])

if __name__ == "__main__":
    main()