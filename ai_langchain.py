from dotenv import load_dotenv
import os

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

system_prompt = """
Hi.I am a Python Programming Language.
It is a fun to work with Python language.
It is very easy to build AI applications using Python.
Answer in 2-4 sentences.
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
