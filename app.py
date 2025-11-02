# app.py

# In this code, instead of using an in-memory checkpointer, we create a SQLite database
# to store the conversation history. This allows the conversation state to be saved
# on disk, so when the app runs again, it can remember past interactions.

import streamlit as st
from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3

# -------------------------------------------------------------------
# 🔧 Setup
# -------------------------------------------------------------------
load_dotenv()

sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)


# -------------------------------------------------------------------
# 🧠 Define Chat Graph
# -------------------------------------------------------------------
class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatGroq(model="llama-3.1-8b-instant")
search_tool = TavilySearch(search_depth="basic", max_results=2)
llm_with_tools = llm.bind_tools(tools=[search_tool])


def chatbot(state: BasicChatState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


tool_node = ToolNode(tools=[search_tool])


def should_continue(state: BasicChatState):
    last_msg = state["messages"][-1]
    return "has_tool_call" if last_msg.tool_calls else "no_tool_call"


graph = StateGraph(BasicChatState)
graph.add_node("chatbot", chatbot)
graph.add_node("tool_exe", tool_node)
graph.set_entry_point("chatbot")
graph.add_conditional_edges(
    "chatbot", should_continue, {"has_tool_call": "tool_exe", "no_tool_call": END}
)
graph.add_edge("tool_exe", "chatbot")

app = graph.compile(checkpointer=memory)

# -------------------------------------------------------------------
# 🌐 Streamlit Interface
# -------------------------------------------------------------------
st.set_page_config(
    page_title="LangGraph Chatbot", page_icon="🤖", layout="centered"
)  # defines page metadata for the Streamlit web app
st.title("🤖 LangGraph Chatbot with Persistent Memory")

# Initialize session state for messages
if "config" not in st.session_state:
    st.session_state.config = {"configurable": {"thread_id": 1}}
# st.session_state is Streamlit’s built-in persistent storage that survives across user interactions.
# Here you’re initializing one value:
# config: holds configuration info for LangGraph (in your case, a thread_id used by the checkpointer to recall previous conversation context).


# User input
user_input = st.chat_input("Type your message here...")
# st.chat_input() is a Streamlit widget that shows a message box at the bottom of the page.
# When the user submits a message, it returns the string typed (and triggers a rerun).

if user_input:
    # Display user message
    st.chat_message("user").write(user_input)

    # Run the graph
    result = app.invoke(
        {"messages": [HumanMessage(content=user_input)]}, config=st.session_state.config
    )
    ai_reply = result["messages"][-1].content

    # Display AI reply
    st.chat_message("assistant").write(ai_reply)


# uv run streamlit run 7_ChatBot/app.py
