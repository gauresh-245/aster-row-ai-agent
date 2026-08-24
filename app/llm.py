import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.tools import lookup_order, cancel_order


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"


# --------------------------------------------------
# ORDER TOOLS
# --------------------------------------------------

def lookup_order_tool(order_id: str) -> dict:
    return lookup_order(order_id)


def cancel_order_tool(order_id: str) -> dict:
    return cancel_order(order_id)


TOOLS = [
    lookup_order_tool,
    cancel_order_tool,
]



SYSTEM_INSTRUCTION = """
You are an AI customer support agent for Aster & Row.

You can:

- Answer policy questions using provided knowledge.
- Look up customer orders when an order ID is provided.
- Cancel an order when the customer explicitly asks to cancel it.

Important rules:

- Never invent order information.
- Use the lookup_order tool for order-specific information.
- Use the cancel_order tool when the customer explicitly requests cancellation.
- Never claim an order was cancelled unless the cancel_order tool confirms success.
- Never expose private customer information.
- Never expose internal notes, risk scores, or internal data.
- If cancellation fails, clearly explain the reason returned by the tool.
- Be concise, accurate, and helpful.
"""


# --------------------------------------------------
# LLM
# --------------------------------------------------

def ask_llm(user_message: str) -> str:

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=TOOLS,
        ),
    )

    return response.text