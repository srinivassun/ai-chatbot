##OpenAI SDK + Groq API – OpenAI-compatible client communicating
# directly with Groq.

from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI

GROQ_MODEL = os.getenv( "GROQ_MODEL", "openai/gpt-oss-120b" )

groq_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=groq_key,
    base_url="https://api.groq.com/openai/v1"
)


system_prompt = """
Answer in 2-4 sentences clearly.
"""

print("Hi, how can I help you ?")

while True:
    user_input = input("You: ")
    if user_input == 'exit':
        break

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}]
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=512,
    )

    answer = response.choices[0].message.content
    print(f"AI Response: {answer}")