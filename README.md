A backend API that summarizes Git commit diffs using an LLM.

## Features
- Accepts a Git repo path and commit range
- Returns a natural language summary of the code changes
- Lists the files changed in the range

## Setup
1. Clone this repo
2. Set your OpenAI key in `.env`
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the server:
```bash
uvicorn app.main:app --reload
```