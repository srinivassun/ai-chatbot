from dotenv import load_dotenv
import os

load_dotenv()
from langchain.agents import create_agent

PROVIDER = os.getenv("PROVIDER")
MODEL = "groq:openai/gpt-oss-120b"   # check console.groq.com for current IDs
api_key = os.getenv("GROQ_API_KEY")

system_prompt = """
 You are a helpful assistant. Always answer the questions very clearly and completely in your answer.
"""

agent = create_agent(
    model=MODEL,
    # Tighter prompt: force the model to actually state the result so we don't
    # get vague answers like "that's the current weather".
    system_prompt=system_prompt
)

while True:
    user_input = input("Question: ")
    if user_input == 'exit':
        break
    response = agent.invoke({"messages": user_input})
    print(f"Answer: {response['messages'][-1].content}")