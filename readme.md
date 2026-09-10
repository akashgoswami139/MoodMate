# MoodMate 🤖

MoodMate is a mini AI chatbot built with **LangChain, OpenRouter, and Streamlit** that lets users choose the personality of the AI before starting a conversation.

Choose between:

- 😄 Happy
- 😢 Sad
- 😡 Angry

Each mood uses a different system prompt, giving the chatbot a different personality while maintaining conversational history.

## ✨ Features

- 🎭 Three AI personalities: Happy, Sad, and Angry
- 💬 Conversational chat history
- 🧠 LangChain message-based architecture
- 🌐 OpenRouter LLM integration
- 🎨 Mood-based Streamlit UI
- 🔄 Switching mood automatically starts a fresh conversation
- 🔐 API key stored using environment variables
- ✨ Animated mood-based background and UI
- 👨‍💻 Built by Akash Goswami

## 🛠️ Tech Stack

- **Python**
- **LangChain**
- **LangChain OpenRouter**
- **OpenRouter**
- **Streamlit**
- **python-dotenv**

## 📂 Project Structure

```text
MoodMate/
│
├── app.py
├── agent.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md