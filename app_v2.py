import os
import fitz  # This is the PyMuPDF library
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_pdfs_from_directory(directory_path):
    """Reads all PDF files from a directory and extracts their text."""
    knowledge_base = ""
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory_path, filename)
            try:
                with fitz.open(filepath) as doc:
                    for page in doc:
                        knowledge_base += page.get_text()
                knowledge_base += "\n\n" # Add a separator between documents
                print(f"Successfully read {filename}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return knowledge_base

def ask_assistant(question, knowledge_base):
    """Asks the assistant a question with the provided knowledge base."""
    # Note: We give the model a larger context window with gpt-3.5-turbo-16k
    # if the text from all PDFs is very long.
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specializing in the FDA's drug approval process. Answer the user's questions based ONLY on the provided text from the PDF documents. If the answer is not in the text, say that you cannot find the answer in the provided documents."},
            {"role": "user", "content": f"Here is the information I have about the FDA drug approval process from several documents:\n\n{knowledge_base}\n\nPlease answer the following question:\n{question}"}
        ]
    )
    return response.choices[0].message.content

def main():
    """Main function to run the assistant."""
    print("Loading knowledge base from PDF documents...")
    # The name of our new folder is 'data_pdfs'
    fda_knowledge = load_pdfs_from_directory("data_pdfs")

    if not fda_knowledge:
        print("No knowledge base loaded. Make sure your PDFs are in the 'data_pdfs' folder.")
        return

    print("\nWelcome to the Advanced FDA Drug Approval Assistant!")
    print("My knowledge comes from the PDF documents you provided.")
    print("Ask a question (or type 'quit' to exit).")

    while True:
        user_question = input("\nYour question: ")
        if user_question.lower() == 'quit':
            break

        answer = ask_assistant(user_question, fda_knowledge)
        print(f"\nAssistant: {answer}")

if __name__ == "__main__":
    main()