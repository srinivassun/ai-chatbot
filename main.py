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
Hi.I am a Software Engineer learning python.
It is a fun to work with Python language.
Answer in 2-6 sentences.
"""
response = llm.invoke([
    {"role":"system", "content":system_prompt},
    {"role":"user", "content":"Hi Python, tip of the day?"}])

print(response.content)