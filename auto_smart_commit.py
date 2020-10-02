#!/usr/bin/env python3

import re
import sys
from subprocess import check_output
from typing import NoReturn, Optional


def run_command(command: str) -> str:
    try:
        stdout: str = check_output(command.split()).decode("utf-8").strip()
    except Exception:
        stdout = ""
    return stdout


def current_git_branch_name() -> str:
    return run_command("git symbolic-ref --short HEAD")


def extract_jira_issue_key(message: str) -> Optional[str]:
    project_key, issue_number = r"[A-Z]{2,}", r"[0-9]+"
    match = re.search(f"{project_key}-{issue_number}", message)
    if match:
        return match.group(0)
    return None

def main() -> NoReturn:
    # https://confluence.atlassian.com/fisheye/using-smart-commits-960155400.html
    # Exit if the branch name does not contain a Jira issue key.
    git_branch_name = current_git_branch_name()
    jira_issue_key = extract_jira_issue_key(git_branch_name)
    if not jira_issue_key:
        sys.exit(0)

    # Read the commit message.
    commit_msg_filepath = sys.argv[1]
    with open(commit_msg_filepath) as f:
        commit_msg = f.read()

    # Build the new commit message
    if not commit_msg.startswith(jira_issue_key):
        commit_msg = f"{jira_issue_key} | {commit_msg}"

    # Override commit message.
    with open(commit_msg_filepath, "w") as f:
        f.write(commit_msg)
    sys.exit(0)


if __name__ == "__main__":
    main()
