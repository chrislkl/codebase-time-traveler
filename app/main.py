from fastapi import FastAPI, HTTPException
from app.models import DiffRequest, DiffSummary, GitHubRequest, CommitSummary
from app.git_utils import get_git_diff, clone_github_repo, get_commit_summaries
from app.summarizer import summarize_diff
import tempfile
import shutil
import os

app = FastAPI()

repo_cache: dict[str, str] = {}

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
    try:
        if request.repo_url in repo_cache and os.path.exists(repo_cache[request.repo_url]):
            repo_path = repo_cache[request.repo_url]
        else:
            temp_dir = tempfile.mkdtemp()
            repo_path = clone_github_repo(request.repo_url, temp_dir)
            repo_cache[request.repo_url] = repo_path

        summaries = get_commit_summaries(repo_path, request.max_commits)
        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))