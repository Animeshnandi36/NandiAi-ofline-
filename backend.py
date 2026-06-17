from typing import Dict, List, Generator, Any
import logging

# LangChain/Ollama imports may vary by package versions.
# If these imports fail, install the proper versions or adjust names.
try:
    from langchain_ollama import ChatOllama
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, AIMessage
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
    HumanMessage = None
    AIMessage = None

# Minimal robust in-memory session store:
_store: Dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Return an InMemoryChatMessageHistory object for the session."""
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory() if InMemoryChatMessageHistory is not None else None
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
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

def get_response(user_input: str, session_id: str) -> Generator[str, None, None]:
    """
    Returns a generator yielding chunks of text (strings).
    The UI expects an iterable of text parts to stream.
    """
    # Add user message to session history
    history = get_session_history(session_id)
    if history is not None and HumanMessage is not None:
        history.add_message(HumanMessage(content=user_input))

    # If LangChain conversation is available, attempt to stream from it.
    full_response = ""
    try:
        if conversation is not None:
            # Many LangChain runnables provide .stream or iterator-like outputs; attempt to use it.
            stream_output = conversation.stream({"input": user_input}, config={"configurable": {"session_id": session_id}})
            # If it's an iterable/generator, yield its chunks
            if hasattr(stream_output, "__iter__"):
                for chunk in stream_output:
                    # Handle different chunk types
                    if isinstance(chunk, str):
                        text = chunk
                    elif hasattr(chunk, 'content'):
                        text = chunk.content
                    else:
                        text = str(chunk)
                    full_response += text
                    yield text
            else:
                # Not iterable: convert to string and yield once
                text = str(stream_output)
                full_response += text
                yield text
        else:
            # Fallback: simple echo responder for offline testing
            reply = "Nandi Ai here. (LangChain not initialized.) You asked: " + user_input
            # yield in two chunks to simulate streaming
            mid = len(reply) // 2
            full_response = reply
            yield reply[:mid]
            yield reply[mid:]
    except Exception as exc:
        # Yield an error message so the UI shows something
        error_text = f"[Nandi Ai error: {exc}]"
        logging.exception("Failed to get response from LLM/chain.")
        full_response = error_text
        yield error_text
    finally:
        # Save the assistant's response to session history
        history = get_session_history(session_id)
        if history is not None and AIMessage is not None and full_response:
            history.add_message(AIMessage(content=full_response))
