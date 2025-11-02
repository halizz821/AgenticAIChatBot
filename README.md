# AgenticAIChatBot

# Agentic AI Chatbot 🤖

An **Agentic AI Chatbot** built using **LangGraph** and **LangChain**, capable of reasoning, remembering past interactions, and searching the web through the **Tavily Search API**.

This project demonstrates how to design an **agentic conversational AI** with persistent memory using **LangGraph’s StateGraph** and **SQLite checkpointing**, while providing an intuitive **Streamlit interface** for real-time chat.

---

## 🧠 Overview

This chatbot integrates several cutting-edge AI components:

- **LangGraph** — for managing agent state, tool calls, and conversation flow.  
- **LangChain** — for message handling, LLM integration, and tool binding.  
- **Groq LLM (LLaMA 3.1)** — a fast inference model for generating intelligent responses.  
- **TavilySearch** — to enable the agent to fetch live web information.  
- **SQLite checkpoint memory** — so your conversations persist across sessions.  
- **Streamlit UI** — a clean, chat-style interface to interact with the agent.

> 💡 The chatbot behaves like a memory-augmented, reasoning agent that can use external tools (search) and resume its context between runs.

---

## ⚙️ Environment Setup

Before running the chatbot, create a `.env` file in the project root and add your API keys:

```bash
TAVILY_API_KEY = "paste_your_tavily_key_here"
GROQ_API_KEY = "paste_your_groq_key_here"



## Installation
To install dependencies and set up the environment:

1. Install **uv** (a project environment manager):
   ```bash
   pip install uv
   ```
2. Navigate to the project folder and run:
   ```bash
   uv sync
   ```
   This will install all dependencies and create a new environment for the project.
   

## 🚀 How to Run
Launch the chatbot with Streamlit.
   ```bash
   uv run streamlit run app.py
   ```
The app will open automatically in your browser.   

## 🙌 Acknowledgements
Thanks to  [harishneel1](https://github.com/harishneel1) for its course on [LangGraph](https://www.youtube.com/watch?v=Y3dbzuQBnUw&t=11278s)
that inspired this project.
   
   
   
