from dotenv import load_dotenv
import os
from groq import Groq
load_dotenv()
# Initialize Groq client
groq_key = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv( "GROQ_MODEL", "openai/gpt-oss-120b" )

client = Groq(
    api_key=groq_key
)
system_prompt = """
Answer in 2-4 sentences clearly.
"""

print("Hi, how can I help you ?")
# Send request to Groq
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