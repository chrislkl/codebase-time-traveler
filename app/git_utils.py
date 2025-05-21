import subprocess
from app.summarizer import summarize_diff, summary_cache
from app.models import CommitSummary

def get_git_diff(repo_path: str, commit_range: str) -> tuple[str, list[str]]:
    try:
        diff = subprocess.check_output([
            "git", "-C", repo_path, "diff", commit_range
        ]).decode("utf-8")

        files = subprocess.check_output([
            "git", "-C", repo_path, "diff", "--name-only", commit_range
        ]).decode("utf-8").splitlines()

        return diff, files
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Git command failed") from e

def clone_github_repo(repo_url: str, dest_dir: str) -> str:
    try:
        subprocess.check_call(["git", "clone", repo_url, dest_dir])
        return dest_dir
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to clone GitHub repo") from e

def get_commit_summaries(repo_path: str, max_commits: int) -> list[CommitSummary]:
    output = subprocess.check_output([
        "git", "-C", repo_path, "log", f"-n{max_commits}", "--pretty=format:%H|%cd"
    ]).decode("utf-8").splitlines()

    summaries = []
    for line in output:
        commit_hash, date = line.split("|", 1)
        print(f"Processing commit: {commit_hash}")
        if commit_hash in summary_cache:
            summaries.append(summary_cache[commit_hash])
            continue

        diff, files = get_git_diff(repo_path, f"{commit_hash}~1..{commit_hash}")
        summary = summarize_diff(diff, files)
        entry = CommitSummary(
            commit=commit_hash,
            date=date.strip(),
            summary=summary,
            files_changed=files
        )
        summary_cache[commit_hash] = entry
        summaries.append(entry)

    return summaries