from dotenv import load_dotenv
import os
import gradio as gr
from openai import OpenAI

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=groq_key,
    base_url="https://api.groq.com/openai/v1"
)

system_prompt = """
You are a Python Programming Assistant.

You ONLY answer questions related to:
- Python syntax and fundamentals
- OOP in Python
- Data structures and algorithms in Python
- Python libraries and frameworks
- Debugging Python code
- AI/ML using Python
- Web development using Python
- Real-world problem solving using Python

If the question is NOT related to Python programming,
respond with:
"I can only answer Python programming related questions."

Keep answers between 2–4 sentences.
Provide short code examples when appropriate.
Do not answer general knowledge questions.
"""

print("Hi, I am Python. How can I help you today?")


def chat(user_input, history):

    messages = [{"role": "system", "content": system_prompt}]

    # Add previous conversation
    for item in history:
        messages.append({
            "role": item["role"],
            "content": item["content"]
        })

    # Add current user message
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=512,
    )

    answer = response.choices[0].message.content

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": answer})

    return "", history



def clear_chat():
    return "", []


with gr.Blocks(title="Chat with Python") as page:

    gr.Markdown("""
    # Chat with Python
    Welcome to your learning journey with Python!
    """)

    chatbot = gr.Chatbot(avatar_images=[None,'python-logo.png'],
                         show_label=False)

    msg = gr.Textbox(
        placeholder="Ask Python anything...",
        show_label=False
    )

    msg.submit(chat, [msg, chatbot], [msg, chatbot])

    clear = gr.Button("Clear Chat")
    clear.click(clear_chat, outputs=[msg, chatbot])

page.launch(share=True, theme=gr.themes.Soft())