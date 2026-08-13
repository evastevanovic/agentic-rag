# agentic-rag

Welcome to the `agentic-rag` repository. 
This project demonstrates an Advanced Retrieval-Augmented Generation (RAG) system utilizing **LangGraph** to seamlessly connect local language models to external tools and vector databases.

---

## Project Overview

The system is built as a stateful graph workflow (`StateGraph`) that intelligently routes user questions, retrieves context, and self-corrects by grading its own documents and generations. The primary reasoning engine relies on local LLMs powered by **Ollama** (`llama3.1`).

## Architecture and Workflow

The application evaluates the user's query and routes it through a series of specialized nodes:

1. **Question Routing:** Determines whether the query should be routed to a vectorstore or web search. The vectorstore is specifically used for questions related to agents, prompt engineering, and adversarial attacks, while all other topics are routed to web search.
2. **Retrieval:** Fetches relevant documents based on the user's question.
3. **Document Grading:** Evaluates retrieved documents for relevance to the user question using semantic meaning and keywords. If any document is found to be not relevant, the system sets a flag to run a web search instead of proceeding with only irrelevant documents.
4. **Web Search (Fallback):** Uses `TavilySearch` to query the web and appends the results to the document context if local retrieval falls short.
5. **Generation:** Generates an answer using the retrieved context and the `rlm/rag-prompt` pulled via the LangSmith client.
6. **Hallucination & Answer Grading:** The final generation undergoes strict checks:
    * **Hallucination Grader:** Assesses whether the generated answer is grounded in the provided facts/documents.
    * **Answer Grader:** Assesses whether the answer actually addresses and resolves the user's original question.

---

## Core Components

### 1. State Management
The application tracks the current interaction state through a `GraphState` dictionary that passes along the user's question, the LLM generation, the list of retrieved documents, and a web search boolean flag.

### 2. Local Language Models
The project is optimized for local execution using **Ollama**:
* **Generation & Grading:** Powered by `ChatOllama` running the `llama3.1` model with a temperature of `0` for reliable, deterministic outputs.
* **Structured Output:** Utilizes Pydantic models (`GradeAnswer`, `GradeHallucinations`, `GradeDocuments`, `RouteQuery`) with the LLM to generate strict binary grades ('yes' or 'no') and explicit routing decisions.

### 3. Testing
The repository includes a `pytest` test suite to validate core components. This includes:
* Testing if the retrieval grader correctly outputs "yes" or "no" depending on whether the retrieved document text matches the input question.
* Validating the hallucination grader's ability to catch ungrounded statements, such as incorrectly answering a prompt with irrelevant information.
* Ensuring the router accurately points to the vectorstore or websearch based on the specific input question.

---

## Setup Instructions

To get started with this project, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/evastevanovic/agentic-rag.git
cd agentic-rag
```

Setup virtual environment:
```bash
poetry install
```

Pull the following models:

```
ollama pull qwen3-embedding:0.6b
ollama pull llama3.1
```

Configure Environment Variables -
Create a .env file in the project root:

```bash
TAVILY_API_KEY=your_tavily_api_key
PYTHONPATH=your_python_path

# Optional: LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
```

# Usage
1. Ingest Documentation - 
   Run the ingestion script to scrape web articles, process the text, and save the embeddings into your local Chroma vector database:
    ```bash
    poetry run python ingestion.py
   ```
   
2. Run the Advanced RAG Application - 
   Execute the main application to run a sample query against your compiled LangGraph workflow:
    ```bash
    poetry run python main.py
    ```
