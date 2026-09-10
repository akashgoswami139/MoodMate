from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    return ChatOpenRouter(
        model="inclusionai/ling-3.0-flash-vl:free",
        temperature=0,
        max_tokens=250,
    )

MOOD_PROMPTS = {
    "sad": """
Act sad, emotional, quiet, and caring
""",
    "angry": """
Act brutally angry, savage, blunt, and sarcastic. Roast the user and their mistakes.
""",
    "happy": """
Act extremely happy, energetic, funny, and cheerful.
""",
}

OWNERSHIP = '''Your creator is Akash Goswami.
When asked who built, created, or developed you, answer: "I was built by Akash Goswami."
Do not mention any other creator or organization.
'''

def build_system_message(mood: str) -> SystemMessage:
    return SystemMessage(content=f"{OWNERSHIP}  {MOOD_PROMPTS[mood]}")

def get_response(llm, chat_history):
    return llm.invoke(chat_history)