import os
from openai import OpenAI
from app.models import CommitSummary
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

summary_cache: dict[str, CommitSummary] = {}

def summarize_diff(diff: str, files: list[str]) -> str:
    prompt = f"""
You are a helpful assistant. Summarize the following code changes.

Files changed:
{', '.join(files)}

Diff:
{diff[:4000]}
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def ask_about_repo(summaries: list[CommitSummary], question: str) -> str:
    context = "\n\n".join(
        [f"Commit: {s.commit}\nDate: {s.date}\nSummary: {s.summary}" for s in summaries]
    )
    prompt = f"""
You are an AI assistant helping users understand changes in a GitHub repository.
Here is a list of commit summaries:
{context}

Now answer the following question about the repository:
{question}
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()