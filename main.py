from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_key,
    temperature=0.5
)
system_prompt = """
Hi.I am a Python Programming Language.
It is a fun to work with Python language.
It is very easy to build AI applications using Python.
Answer in 2-4 sentences.
"""
print("Hi, I am Python how can I help you today")

while True:
    user_input = input("You: ")
    if user_input == 'exit':
        break
    response = llm.invoke([
    {"role":"system", "content":system_prompt},
    {"role":"user", "content": user_input}])
    print(f"Python Response: {response.content}")