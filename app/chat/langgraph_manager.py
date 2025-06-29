import uuid
from typing import Annotated, Dict, List, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from loguru import logger

from app.config import (
    GOOGLE_API_KEY,
    LLM_MODEL_NAME,
)
from app.vectorstore.faiss_store import SessionVectorStore


# State: messages (list of BaseMessage)
class ChatState(TypedDict):
    """State of our Chatbot. This holds the conversational history with the chatbot."""

    messages: Annotated[List[BaseMessage], add_messages]
    query: str
    context: str
    session_id: str


# Retrieval Node
def retrieve_context(state: ChatState) -> ChatState:
    logger.debug(
        f"-----STATE----- at the BEGINNIG of the function-> retrieve_context: {state}"
    )
    logger.debug(f"Type of state: {type(state)}")

    session_id = state["session_id"]
    retriever = SessionVectorStore.get_retriever(session_id)
    logger.debug(f"The retriver object: {retriever}")
    if retriever is None:
        context = "[No documents indexed yet.]"
    else:
        docs = retriever.get_relevant_documents(state["query"])
        context = "\n".join([doc.page_content for doc in docs])

    # Store context for use in call_gemini
    state["context"] = context
    logger.debug(
        f"-----STATE----- at the END of the function-> retrieve_context: {state}"
    )
    return state


# LLM call Node
def call_gemini(state: ChatState) -> ChatState:
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME, google_api_key=GOOGLE_API_KEY)

    messages = [
        SystemMessage(
            content="You are a helpful AI assistant. Respond concisely and accurately using the provided context."
        ),
        HumanMessage(content=f"Context:\n{state['context']}\n\nUser: {state['query']}"),
    ]
    response = llm.invoke(messages)
    logger.info(f"The response from the LLM: {response}")

    state["messages"].append(HumanMessage(content=state["query"]))

    state["messages"].append(response)

    return state


graph = StateGraph(ChatState)
graph.add_node("retrieve_context", retrieve_context)
graph.add_node("call_gemini", call_gemini)

graph.add_edge(START, "retrieve_context")
graph.add_edge("retrieve_context", "call_gemini")
graph.add_edge("call_gemini", END)

# MemorySaver for checkpointing
memory = MemorySaver()
langgraph_flow = graph.compile(checkpointer=memory)


class LangGraphManager:
    def start_session(self) -> str:
        session_id = str(uuid.uuid4())
        return session_id

    def chat(self, session_id: str, user_input: str) -> Dict:
        logger.debug(
            f"LangGraphManager.chat called with session_id={session_id}, user_input={user_input}"
        )
        config = {"configurable": {"thread_id": session_id, "checkpoint_ns": "default"}}

        logger.debug(f"User Query: {user_input}")
        # Running the graph
        result = langgraph_flow.invoke(
            {"query": user_input, "session_id": session_id}, config=config
        )
        logger.info(f"Final response from the LLM: {result['messages']}")

        history = []
        for m in result["messages"]:
            if isinstance(m, HumanMessage):
                history.append({"role": "user", "content": m.content})
            elif isinstance(m, AIMessage):
                history.append({"role": "bot", "content": m.content})
        return {
            "history": history,
            "session_id": session_id,
        }


langgraph_manager = LangGraphManager()
