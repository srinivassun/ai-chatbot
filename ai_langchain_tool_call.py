from dotenv import load_dotenv
import os

load_dotenv()

PROVIDER = os.getenv("PROVIDER")

if PROVIDER == "groq":
    MODEL = "groq:openai/gpt-oss-120b"   # check console.groq.com for current IDs
    REQUIRED_KEY = "GROQ_API_KEY"
elif PROVIDER == "gemini":
    MODEL = "google_genai:gemini-2.0-flash"
    REQUIRED_KEY = "GOOGLE_API_KEY"
else:  # openai
    MODEL = "openai:gpt-4o-mini"
    REQUIRED_KEY = "OPENAI_API_KEY"

key = os.getenv(REQUIRED_KEY)

system_prompt = """
 You are a helpful assistant. Use the available tools when needed.
 Always state the final result clearly and completely in your answer.
"""

def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"The weather in {city} is sunny, 28 degrees C."


def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

def get_trade_valuation(trade_id):
    """Get the trade valuation summary."""
    return {
        "trade_id": trade_id,
        "valuation": 1250000,
        "currency": "USD"
    }

def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

TOOLS = [get_weather, add, multiply, get_trade_valuation]

from langchain.agents import create_agent

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    # Tighter prompt: force the model to actually state the result so we don't
    # get vague answers like "that's the current weather".
    system_prompt=system_prompt
)

print("Hi, how can I help you today")

while True:
    user_input = input("You: ")
    if user_input == 'exit':
        break
    response = agent.invoke({"messages": user_input})
    for msg in response["messages"]:
        if msg.type == "ai" and getattr(msg, "tool_calls", None):
            for tc in msg.tool_calls:
                print(f"   [tool call]   {tc['name']}({tc['args']})")
        elif msg.type == "tool":
            print(f"   [tool result] {msg.content}")

    print(f"A: {response['messages'][-1].content}")
