

from langsmith import Client
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

# Initialize your LLM
llm = ChatOllama(temperature=0, model="llama3.1")

# 1. Initialize the modern LangSmith client (replaces 'hub')
client = Client()

# 2. Pull the prompt (returns a proper Runnable object)
prompt = client.pull_prompt("rlm/rag-prompt", dangerously_pull_public_prompt=True)

from langchain_core.output_parsers import StrOutputParser
#from langchain_openai import ChatOpenAI
#from langchain_ollama import ChatOllama

#llm = ChatOllama(temperature = 0, model="llama3.1")

#prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()

