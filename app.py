import streamlit as st
import uuid
from backend import get_response

st.set_page_config(page_title="Nandi Ai [OFFLINE]", page_icon="🦋")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.title("🛡️ Security Monitor")
    st.success("Internet: DISCONNECTED")
    st.success("Data Encryption: LOCAL_ONLY")
    st.info("Model: LLaMA 2:7b (local)")
    st.caption(f"Session: {st.session_state.session_id[:8]}...")
    if st.button("Clear Context Window"):
        st.session_state.messages = []
        st.rerun()

st.title("🔒 Nandi Ai — Secure Generative AI Chat Assistant")
st.caption("Proprietary Information Processing Environment | v1.0")

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter secure query..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Stream the assistant response into the chat UI and build full_response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # get_response is expected to be a generator yielding string chunks
            for chunk in get_response(prompt, st.session_state.session_id):
                # Some backends yield dicts or bytes; normalize to string
                if chunk is None:
                    continue
                text = chunk.decode() if isinstance(chunk, (bytes, bytearray)) else str(chunk)
                full_response += text
                placeholder.markdown(full_response)
        except Exception as e:
            err_msg = f"Error generating response: {e}"
            placeholder.markdown(err_msg)
            full_response = err_msg

    # Save the completed assistant message
    st.session_state.messages.append({"role": "assistant", "content": full_response})
