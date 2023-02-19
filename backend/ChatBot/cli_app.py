import pickle
from query_data import get_chain

with open("vectorstore.pkl", "rb") as f:
    vectorstore = pickle.load(f)

def ask_question(question, chat_history):
    result = qa_chain({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    return result["answer"].strip(), chat_history

if __name__ == "__main__":
    qa_chain = get_chain(vectorstore)
    chat_history = []
    print("Chat with your docs!")
    while True:
        print("Human:")
        question = input()
        answer, chat_history = ask_question(question, chat_history)
        print("AI:")
        print(answer.strip())