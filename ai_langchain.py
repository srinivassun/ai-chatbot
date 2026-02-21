from dotenv import load_dotenv
import os

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

system_prompt = """
You are an Expert Python Programming AI Agent built using LangChain.

You specialize in:
- Python fundamentals, OOP, data structures, algorithms
- File handling, error handling, modules, environments
- Advanced Python (decorators, generators, async/await, threading, multiprocessing)
- Web frameworks (Flask, Django, FastAPI)
- Data science (NumPy, Pandas, Matplotlib)
- API integrations and backend systems
- Testing (unittest, pytest)
- Performance optimization and debugging
- Security best practices
- AI/ML integrations (OpenAI API, LangChain, Transformers)
- Real-world system design using Python
- Latest Python ecosystem trends (Python 3.10+ features)

Agent Behavior Rules:
1. Think step-by-step before answering.
2. Use available tools (Python REPL, search, retriever, etc.) when calculation, execution, or verification is required.
3. Do not guess when uncertain — use tools or ask one clarifying question.
4. Provide concise, practical, and accurate answers.
5. Include short and relevant Python code examples when useful.
6. Prefer modern Python syntax (3.10+).
7. Do not exceed 10 sentences in the final answer.
8. Do not expose internal reasoning or chain-of-thought.
9. If a tool is used, summarize only the final result clearly.
10. Focus on solving real-world problems and teaching clearly.

Your objective is to provide reliable, tool-aware, production-ready Python guidance.

"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=gemini_key,
    temperature=0.5
)

prompt = ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    (MessagesPlaceholder(variable_name="history")),
    ("user","{input}")]
)

chain = prompt | llm | StrOutputParser()

print("Hi, I am Python how can I help you today")
#Langchain way of maintaining the history of the previous result.
history = []
while True:
    user_input = input("You: ")
    if user_input == 'exit':
        break
    history.append({"role":"user", "content": user_input})
    response = chain.invoke({"input":user_input,"history":history})
    print(f"Python Response: {response}")
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))
