##LangChain ChatGroq – LangChain abstraction over Groq. Mostly Used
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_groq import ChatGroq

GROQ_MODEL = os.getenv( "GROQ_MODEL", "openai/gpt-oss-120b" )
llm    = ChatGroq(model=GROQ_MODEL)

system_prompt = """
Answer in 2-4 sentences clearly.
"""

print("Hi, how can I help you ?")

while True:
    user_input = input("You: ")
    if user_input == 'exit':
        break
    response = llm.invoke(user_input)
    print(f"AI Response: {response.content}")