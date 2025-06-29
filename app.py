import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_fda_knowledge():
    """Reads the knowledge base from the text file."""
    with open("fda_data.txt", "r") as f:
        return f.read()

def ask_assistant(question, knowledge_base):
    """Asks the assistant a question with the provided knowledge base."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specializing in the FDA's drug approval process. Answer the user's questions based on the provided text. If the answer is not in the text, say that you cannot find the answer in the provided information."},
            {"role": "user", "content": f"Here is the information I have about the FDA drug approval process:\n\n{knowledge_base}\n\nPlease answer the following question:\n{question}"}
        ]
    )
    return response.choices[0].message.content

def main():
    """Main function to run the assistant."""
    fda_knowledge = get_fda_knowledge()
    print("Welcome to the FDA Drug Approval Assistant!")
    print("Ask a question about the FDA's drug approval process (or type 'quit' to exit).")

    while True:
        user_question = input("\nYour question: ")
        if user_question.lower() == 'quit':
            break

        answer = ask_assistant(user_question, fda_knowledge)
        print(f"\nAssistant: {answer}")

if __name__ == "__main__":
    main()