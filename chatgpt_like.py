import streamlit as st
import os
import json
from datetime import datetime, timedelta
from openai import OpenAI

# -----------------------
# Configuration
# -----------------------
# Instantiate the OpenAI client. It will use the OPENAI_API_KEY from the environment.
client = OpenAI()

HISTORY_FILE = "chat_history.json"

MODEL_OPTIONS = [
    "gpt-4",
    "gpt-4-32k",
    "gpt-4-turbo"
]

# -----------------------
# Helper Functions
# -----------------------
def load_history():
    """Load all sessions from local JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    """Save all sessions to local JSON file."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def categorize_sessions_by_date(sessions):
    """Group sessions by Today, Previous 7 days, Previous 30 days."""
    now = datetime.utcnow()
    today = []
    seven_days = []
    thirty_days = []

    for i, s in enumerate(sessions):
        ts = datetime.fromisoformat(s["timestamp"])
        delta = now - ts
        if delta.days < 1:
            today.append((i, s))
        elif delta.days < 7:
            seven_days.append((i, s))
        elif delta.days < 30:
            thirty_days.append((i, s))

    return {
        "Today": today,
        "Previous 7 days": seven_days,
        "Previous 30 days": thirty_days
    }

def generate_response_stream(messages, model_name, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stream):
    """
    Call the OpenAI ChatCompletion endpoint using the new client interface.
    If stream=True, yields tokens as they arrive.
    If stream=False, yields the full message once complete.
    """
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stream=stream
    )

    if stream:
        # Streaming mode: yield tokens as they come in
        for chunk in response:
            if "choices" in chunk:
                delta = chunk["choices"][0]["delta"]
                if "content" in delta:
                    yield delta["content"]
    else:
        # Non-streaming mode: just yield the full response
        full_answer = response.choices[0].message["content"]
        yield full_answer

# -----------------------
# Streamlit App
# -----------------------
st.set_page_config(page_title="ChatGPT-like App", page_icon="💬", layout="wide")
st.title("ChatGPT-like Interface")

history = load_history()

# Sidebar for settings and history navigation
st.sidebar.title("Settings & History")

selected_model = st.sidebar.selectbox("Select Model:", MODEL_OPTIONS, index=2)  # "gpt-4-turbo" as default

# According to the OpenAI docs for ChatCompletion:
# - temperature: 0 to 2
# - max_tokens: up to model limit
# - top_p: 0 to 1
# - frequency_penalty: -2 to 2
# - presence_penalty: -2 to 2
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
max_tokens = st.sidebar.number_input("Max Tokens", min_value=1, max_value=32768, value=256, step=1)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 1.0, 0.05)
frequency_penalty = st.sidebar.slider("Frequency Penalty", -2.0, 2.0, 0.0, 0.1)
presence_penalty = st.sidebar.slider("Presence Penalty", -2.0, 2.0, 0.0, 0.1)
stream_response = st.sidebar.checkbox("Stream Response", value=True)

# New session creation
st.sidebar.subheader("Create a New Session")
new_session_heading = st.sidebar.text_input("Session Heading", placeholder="e.g. 'Brainstorming Ideas'")
create_session = st.sidebar.button("Start New Session")

if create_session and new_session_heading.strip():
    new_session = {
        "heading": new_session_heading.strip(),
        "timestamp": datetime.utcnow().isoformat(),
        "messages": []
    }
    history.append(new_session)
    save_history(history)

# Display existing sessions grouped by time
st.sidebar.markdown("### Your Sessions")
grouped = categorize_sessions_by_date(history)

def display_session_links(label, sessions_list):
    if sessions_list:
        st.sidebar.markdown(f"**{label}:**")
        for i, sess in sessions_list:
            st.sidebar.write(
                f"[{sess['heading']}]("
                f"?session_id={i})"
            )

display_session_links("Today", grouped["Today"])
display_session_links("Previous 7 days", grouped["Previous 7 days"])
display_session_links("Previous 30 days", grouped["Previous 30 days"])

# Determine which session is active
session_id = st.experimental_get_query_params().get("session_id", [None])[0]
if session_id is not None:
    try:
        session_id = int(session_id)
    except ValueError:
        session_id = None

current_session = history[session_id] if (session_id is not None and 0 <= session_id < len(history)) else None

if current_session is None and history:
    st.info("Select a session from the sidebar or create a new one.")
elif current_session is None and not history:
    st.info("No sessions yet. Create a new one from the sidebar.")
else:
    # Display current session heading
    st.header(current_session["heading"])

    # Display conversation so far
    for msg in current_session["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**User:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")
        st.markdown("---")

    # Input for new user message
    user_input = st.text_input("Your message:", placeholder="Type your question or prompt...")

    if user_input:
        # Add user message to session
        current_session["messages"].append({"role": "user", "content": user_input})
        save_history(history)

        # Prepare placeholder for assistant's response
        assistant_placeholder = st.empty()

        tokens_accumulator = ""
        for token in generate_response_stream(
            current_session["messages"],
            selected_model,
            temperature,
            max_tokens,
            top_p,
            frequency_penalty,
            presence_penalty,
            stream_response
        ):
            tokens_accumulator += token
            assistant_placeholder.markdown(f"**Assistant:** {tokens_accumulator}")

        # After receiving the entire answer, add assistant message
        current_session["messages"].append({"role": "assistant", "content": tokens_accumulator})
        save_history(history)
