from typing import Dict, List, Generator, Any
import logging

# LangChain/Ollama imports may vary by package versions.
# If these imports fail, install the proper versions or adjust names.
try:
    from langchain_ollama import ChatOllama
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory
except Exception:
    # Provide clear error for the user to adjust dependencies
    logging.exception("LangChain or Ollama-related imports failed. Verify installed package names/versions.")
    # Fallback dummy objects (so the module can be imported for tests). Replace during real use.
    ChatOllama = None
    ChatPromptTemplate = None
    MessagesPlaceholder = None
    InMemoryChatMessageHistory = None
    RunnableWithMessageHistory = None

# Minimal robust in-memory session store:
_store: Dict[str, List[Dict[str, str]]] = {}

def get_session_history(session_id: str) -> List[Dict[str, str]]:
    """Return a list of messages (dicts with role/content) for the session, trimmed to last 10 messages."""
    if session_id not in _store:
        _store[session_id] = []
    # Trim to last 10 messages (10 user/assistant messages combined -> ~5 turns)
    if len(_store[session_id]) > 10:
        _store[session_id] = _store[session_id][-10:]
    return _store[session_id]

# Model instantiation (ensure ChatOllama is available in your environment)
llm = None
if ChatOllama is not None:
    llm = ChatOllama(model="llama2:7b", temperature=0.3)

# Prompt template
prompt = None
if ChatPromptTemplate is not None:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are Nandi Ai, a secure, offline AI assistant. You run on a local machine. Keep answers concise and respectful."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

# If the LangChain runnable APIs are available, wire them up; otherwise we will fallback
chain = None
conversation = None
if prompt is not None and llm is not None:
    chain = prompt | llm
if chain is not None and RunnableWithMessageHistory is not None:
    conversation = RunnableWithMessageHistory(
        chain,
        lambda sid: InMemoryChatMessageHistory() if InMemoryChatMessageHistory is not None else None,
        input_messages_key="input",
        history_messages_key="history",
    )

def _format_history_for_chain(history: List[Dict[str, str]]) -> List[Any]:
    """
    Convert our simple list-of-dict history into the format your chain expects.
    This function may need adjustment depending on your LangChain version.
    """
    formatted = []
    for msg in history:
        formatted.append((msg["role"], msg["content"]))
    return formatted

def get_response(user_input: str, session_id: str) -> Generator[str, None, None]:
    """
    Returns a generator yielding chunks of text (strings).
    The UI expects an iterable of text parts to stream.
    """
    # Update session store with the user message
    history = get_session_history(session_id)
    history.append({"role": "user", "content": user_input})
    # Keep history trimmed
    if len(history) > 10:
        history[:] = history[-10:]

    # If LangChain conversation is available, attempt to stream from it.
    try:
        if conversation is not None:
            # Many LangChain runnables provide .stream or iterator-like outputs; attempt to use it.
            stream_output = conversation.stream({"input": user_input}, config={"configurable": {"session_id": session_id}})
            # If it's an iterable/generator, yield its chunks
            if hasattr(stream_output, "__iter__"):
                for chunk in stream_output:
                    yield chunk
            else:
                # Not iterable: convert to string and yield once
                yield str(stream_output)
        else:
            # Fallback: simple echo responder for offline testing
            reply = "Nandi Ai here. (LangChain not initialized.) You asked: " + user_input
            # yield in two chunks to simulate streaming
            mid = len(reply) // 2
            yield reply[:mid]
            yield reply[mid:]
    except Exception as exc:
        # Yield an error message so the UI shows something
        error_text = f"[Nandi Ai error: {exc}]"
        logging.exception("Failed to get response from LLM/chain.")
        yield error_text
    finally:
        # Append assistant final placeholder (actual final content appended by the UI)
        # Optionally, save a placeholder back into session history; the UI will save the final text itself.
        pass
