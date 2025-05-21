from fastapi import FastAPI, HTTPException
from models import DiffRequest, DiffSummary, GitHubRequest, CommitSummary, AskRequest, AskResponse
from git_utils import get_git_diff, clone_github_repo, get_commit_summaries
from summarizer import summarize_diff, ask_about_repo
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://gittimeai.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


repo_cache: dict[str, str] = {}
commit_summary_cache: dict[str, list[CommitSummary]] = {}

@app.post("/summarize", response_model=DiffSummary)
def summarize(request: DiffRequest):
    try:
        diff, files = get_git_diff(request.repo_path, request.commit_range)
        summary = summarize_diff(diff, files)
        return DiffSummary(summary=summary, files_changed=files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-github", response_model=list[CommitSummary])
def analyze_github(request: GitHubRequest):
    print("Received repo:", request.repo_url)
    try:
        if request.repo_url in repo_cache and os.path.exists(repo_cache[request.repo_url]):
            repo_path = repo_cache[request.repo_url]
        else:
            temp_dir = tempfile.mkdtemp()
            repo_path = clone_github_repo(request.repo_url, temp_dir)
            repo_cache[request.repo_url] = repo_path

        summaries = get_commit_summaries(repo_path, request.max_commits)
        commit_summary_cache[request.repo_url] = summaries
        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask-question", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        if request.repo_url not in commit_summary_cache:
            raise HTTPException(status_code=400, detail="Repo not analyzed yet. Call /analyze-github first.")
        summaries = commit_summary_cache[request.repo_url]
        answer = ask_about_repo(summaries, request.question)
        return AskResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
