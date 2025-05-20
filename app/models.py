from pydantic import BaseModel
from typing import List

class DiffRequest(BaseModel):
    repo_path: str
    commit_range: str  # e.g., "HEAD~5..HEAD"

class DiffSummary(BaseModel):
    summary: str
    files_changed: List[str]

class GitHubRequest(BaseModel):
    repo_url: str
    max_commits: int = 10

class CommitSummary(BaseModel):
    commit: str
    date: str
    summary: str
    files_changed: List[str]