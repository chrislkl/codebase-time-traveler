from ollama import Client
from app.models import CommitSummary

client = Client()
summary_cache: dict[str, CommitSummary] = {}

def summarize_diff(diff: str, files: list[str]) -> str:
    prompt = f"""
You are a helpful assistant. Summarize the following code changes.

Files changed:
{', '.join(files)}

Diff:
{diff[:4000]}
"""
    response = client.chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content'].strip()