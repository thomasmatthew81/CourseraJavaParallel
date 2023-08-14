# chat_app.py
import streamlit as st

# Global list to store chat history
chat_history = []

def main():
    st.title("GPT Chat App with Streamlit")

    user_input = st.text_input("You: ")

    if st.button("Send"):
        # Append user's message to chat history
        chat_history.append({"user": user_input})

        # Get GPT's response
        response = get_gpt_response(user_input)
        chat_history.append({"gpt": response})

    display_chat()

def get_gpt_response(user_input):
    # This is a dummy function. In a real-world scenario, you'd get a response from GPT.
    return f"I'm a mock GPT. You said: {user_input}"

def display_chat():
    for chat in chat_history:
        if "user" in chat:
            st.write(f"You: {chat['user']}")
        else:
            st.write(f"GPT: {chat['gpt']}")

if __name__ == "__main__":
    main()
