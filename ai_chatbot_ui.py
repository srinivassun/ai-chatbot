from dotenv import load_dotenv
import os
import gradio as gr

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

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

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=gemini_key,
    temperature=1
)

prompt = ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    (MessagesPlaceholder(variable_name="history")),
    ("user","{input}")]
)

chain = prompt | llm | StrOutputParser()

print("Hi, I am Python how can I help you today")

def chat(user_input, hist):
    print(user_input, hist)
    langchain_history = []
    for item in hist:
        if item['role'] == 'user':
            langchain_history.append(HumanMessage(content=item['content']))
        elif item['role'] == 'assistant':
            langchain_history.append(AIMessage(content=item['content']))

    response = chain.invoke({"input": user_input, "history": langchain_history})
    return "",hist + [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response}
        ]

def clear_chat():
    return "",[]

page = gr.Blocks(title="Chat with Python")

with page:
    gr.Markdown(
       """
       # Chat with Python
       Welcome to your learning journey with Python!
       """
    )
    chatbot = gr.Chatbot(avatar_images=[None,'python-logo.png'],
                         show_label=False)
    msg = gr.Textbox(show_label=False, placeholder="Ask Python Anything....")
    msg.submit(chat, [msg, chatbot], [msg, chatbot])
    clear = gr.Button("Clear Chat")
    clear.click(clear_chat,outputs=[msg, chatbot])


page.launch(share=True,
            theme=gr.themes.Soft())