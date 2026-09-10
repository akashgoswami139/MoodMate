import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent import MOOD_PROMPTS, get_llm, build_system_message, get_response

st.set_page_config(page_title="MoodMate", page_icon="🤖", layout="centered")

# Theme (colors/avatar) per mood — purely visual, doesn't touch agent.py's prompts
MOOD_THEME = {
    "happy": {"grad": "#f6d365, #fda085, #ffe259, #ffa751", "avatar": "😄", "accent": "#ff9f43"},
    "sad":   {"grad": "#3a6073, #16222a, #232526, #414345", "avatar": "😢", "accent": "#5b86e5"},
    "angry": {"grad": "#870000, #190a05, #cb2d3e, #ef473a", "avatar": "😡", "accent": "#e74c3c"},
}

with st.sidebar:
    st.markdown("### Choose the AI's mood")
    mood = st.radio("Mood", list(MOOD_PROMPTS.keys()), horizontal=True, label_visibility="collapsed")
    st.markdown("---")
    st.caption("Switching mood starts a fresh chat with a new system prompt.")

theme = MOOD_THEME[mood]

st.markdown(f"""
<style>
@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes glowPulse {{
    0%, 100% {{ box-shadow: 0 0 6px {theme['accent']}66; }}
    50% {{ box-shadow: 0 0 18px {theme['accent']}cc; }}
}}
@keyframes titlePop {{
    0% {{ opacity: 0; transform: scale(0.85); }}
    100% {{ opacity: 1; transform: scale(1); }}
}}

.stApp {{
    background: linear-gradient(-45deg, {theme['grad']});
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
}}

h1#mood-title {{
    text-align: center;
    animation: titlePop 0.6s ease-out;
    color: white;
    text-shadow: 0 2px 12px rgba(0,0,0,0.4);
}}

[data-testid="stChatMessage"] {{
    animation: fadeInUp 0.35s ease-out;
    border-radius: 16px !important;
}}

div[data-testid="stChatInput"] {{
    animation: glowPulse 3s ease-in-out infinite;
    border-radius: 24px;
}}

.corner-credit {{
    position: fixed;
    bottom: 14px;
    right: 18px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.3px;
    color: white;
    background: rgba(0,0,0,0.4);
    padding: 6px 16px;
    border-radius: 999px;
    backdrop-filter: blur(8px);
    animation: glowPulse 3s ease-in-out infinite;
    z-index: 9999;
}}

/* Fixed-contrast panel behind all page content so text never washes out
   against the shifting mood-colored background */
[data-testid="stAppViewContainer"] .main .block-container {{
    background: rgba(0,0,0,0.42);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem 2rem 4rem 2rem;
}}

.block-container, .block-container p, .block-container span,
.block-container label, .block-container li {{
    color: #ffffff !important;
}}

/* Chat bubbles keep their own fixed light background + dark text,
   so messages stay legible no matter what the app background is doing */
[data-testid="stChatMessage"] {{
    background: rgba(255,255,255,0.95) !important;
    padding: 0.75rem 1rem !important;
}}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li {{
    color: #1a1a1a !important;
}}
</style>
<div class="corner-credit">✨ Built by Akash Goswami</div>
""", unsafe_allow_html=True)

st.markdown(f"<h1 id='mood-title'>{theme['avatar']} MoodMate</h1>", unsafe_allow_html=True)
st.caption(f"Currently feeling **{mood}** — switch it anytime from the sidebar.")

# ---------- LLM (built once, logic lives in agent.py) ----------
if "llm" not in st.session_state:
    st.session_state.llm = get_llm()

# Reset chat history whenever the mood changes, same as re-running the script with a new choice
if st.session_state.get("active_mood") != mood:
    st.session_state.active_mood = mood
    st.session_state.chat_history = [build_system_message(mood)]

# ---------- Render existing conversation ----------
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=theme["avatar"]):
            st.markdown(msg.content)

# ---------- Chat input (replaces the CLI input() loop) ----------
user_input = st.chat_input("Feel free to ask anything...")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=theme["avatar"]):
        with st.spinner("Thinking..."):
            response = get_response(st.session_state.llm, st.session_state.chat_history)
        st.markdown(response.content)

    st.session_state.chat_history.append(AIMessage(content=response.content))