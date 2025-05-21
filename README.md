# 🧠 Github Codebase Time Traveler

Github Codebase Time Traveler is an AI-powered web app that allows users to analyze the commit history of any public GitHub repository and ask natural language questions about its development timeline.

For example:
> “When did they refactor the login flow?”  
> “Why was the database layer changed in April 2023?”  
> “When was JWT authentication introduced?”

---

## 🔍 How It Works

1. The user enters a GitHub repository URL and number of commits to analyze.
2. The backend clones the repo (if not already cached).
3. For each commit, it extracts the code diff and summarizes the changes using a local or remote LLM.
4. These summaries are cached.
5. When a user asks a question, the app sends the summaries + question to an LLM to generate a natural-language answer.

---

## 🧰 Tech Stack

### Frontend
- **Next.js (React)** – Interactive UI with repo input and question flow
- **Tailwind CSS** – Simple responsive styling

### Backend
- **FastAPI** – Lightweight, high-performance Python API
- **Git CLI** – For commit history, diffs, and repo cloning
- **Groq API** – Fast, hosted LLaMA 3 model for summarization and question answering
- **In-memory cache** – Speeds up repeat analysis and avoids re-summarizing commits

---

## ✨ Features

- ✅ Analyze any **public GitHub repo**
- ✅ Input number of commits to analyze
- ✅ Ask **natural language questions** about code history
- ✅ Commit summaries are **AI-generated**
- ✅ Repositories and commit data are cached for speed
- ✅ Friendly, responsive UI

---

## 📦 Installation (Local Dev)

### 1. Backend
```bash
cd backend/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your-api-key-here" > .env

uvicorn app.main:app --reload
```
### 1. Frontend
```bash
cd frontend/
npm install
npm run dev
```