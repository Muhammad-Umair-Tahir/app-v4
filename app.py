import streamlit as st
import requests
import streamlit.components.v1 as components


# Add enhanced CSS for chat message alignment
st.markdown("""
<style>
/* Overall chat container styling */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    width: 100%;
}

/* User messages on right side */
[data-testid="chat-message-container-user"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-end !important;
    width: 100% !important;
}

.stChatMessage [data-testid="chatAvatarIcon-user"] {
    margin-left: auto !important;
    margin-right: 0 !important;
}

.stChatMessage [data-testid="chat-message-content-user"] {
    background-color: #D1E7FF !important;
    border-radius: 20px 20px 0 20px !important;
    float: right !important;
    margin-left: auto !important;
    max-width: 80% !important;
    text-align: right !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
}

/* Assistant messages on left side */
[data-testid="chat-message-container-assistant"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    width: 100% !important;
}

.stChatMessage [data-testid="chatAvatarIcon-assistant"] {
    margin-left: 0 !important;
    margin-right: auto !important;
}

.stChatMessage [data-testid="chat-message-content-assistant"] {
    background-color: #F0F2F6 !important;
    border-radius: 20px 20px 20px 0 !important;
    float: left !important;
    margin-right: auto !important;
    max-width: 80% !important;
    text-align: left !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
}

/* Hide file uploader label but keep it accessible for screen readers */
[data-testid="stFileUploader"] label {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Custom styles for file upload in sidebar */
.stSidebar [data-testid="stFileUploader"] {
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("Multi-Agent Architectural Assistant")

API_BASE = "http://127.0.0.1:8000/runs"

# Session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "user_id" not in st.session_state:
    st.session_state.user_id = "streamlit_user"

# Sidebar for user inputs and controls
st.sidebar.header("Settings")

# User ID and Session ID inputs moved to sidebar
entered_user_id = st.sidebar.text_input("User ID", value=st.session_state.user_id)
st.session_state.user_id = entered_user_id

entered_session_id = st.sidebar.text_input("Session ID", value=st.session_state.session_id or "")
if entered_session_id:
    st.session_state.session_id = entered_session_id

# Actions section in sidebar
st.sidebar.header("Actions")

# File uploader moved to sidebar with explicit label and label_visibility
st.sidebar.subheader("Upload Floor Plan")
uploaded_file = st.sidebar.file_uploader(
    label="Upload a floor plan image", 
    type=["png", "jpg", "jpeg", "pdf"],
    help="Supported formats: PNG, JPG, JPEG, PDF"
)

# BOQ button in sidebar
if st.sidebar.button("Generate BOQ"):
    prompt = "Generate the bill of quantities."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generating BOQ..."):
            try:
                response = requests.post(
                    f"{API_BASE}?agent_id=boq_agent",
                    data={
                        "message": prompt,
                        "stream": "false",
                        "session_id": st.session_state.session_id or "",
                        "user_id": st.session_state.user_id
                    }
                )
                result = response.json()
                content = result.get("content", "No response")

                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})
                st.session_state.session_id = result.get("session_id", st.session_state.session_id)

            except Exception as e:
                st.error(f"BOQ error: {e}")

# Create a container for chat history
chat_container = st.container()

# Display chat history with custom styling
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Handle uploaded file processing
if uploaded_file:
    st.session_state.messages.append({"role": "user", "content": f"Uploaded: {uploaded_file.name}"})
    with st.chat_message("user"):
        st.markdown(f"Uploaded: `{uploaded_file.name}`")

    with st.chat_message("assistant"):
        with st.spinner("Analyzing image..."):
            try:
                response = requests.post(
                    f"{API_BASE}?agent_id=visualizer_agent",
                    data={
                        "message": f"Analyze the uploaded floor plan: {uploaded_file.name}",
                        "stream": "false",
                        "session_id": st.session_state.session_id or "",
                        "user_id": st.session_state.user_id
                    },
                    files={"file": (uploaded_file.name, uploaded_file.getvalue())}
                )
                result = response.json()
                content = result.get("content", "No response")

                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})
                st.session_state.session_id = result.get("session_id", st.session_state.session_id)

            except Exception as e:
                st.error(f"Image upload error: {e}")

# Use Streamlit's chat_input for user prompt
if prompt := st.chat_input("Describe your project or ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_BASE}?agent_id=interview_agent",
                    data={
                        "message": prompt,
                        "session_id": st.session_state.session_id or "",
                        "user_id": st.session_state.user_id
                    },
                    timeout=120
                )
                result = response.json()
                content = result.get("content", "No response")
                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})
                # Optionally update session_id if your backend returns it in headers or elsewhere

            except Exception as e:
                st.error(f"Interview error: {e}")