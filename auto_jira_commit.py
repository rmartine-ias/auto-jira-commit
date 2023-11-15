#!/usr/bin/env python3

import re
import sys
from pathlib import Path
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


def added_or_modified_filepaths() -> list[str]:
    return run_command("git diff --cached --name-only --diff-filter=AM").splitlines()


def extract_jira_issue_key(message: str, strict: bool = False) -> Optional[str]:
    key_regex = "[a-zA-Z]{2,10}-[0-9]{1,6}"
    if strict:  # Reduce false positives for fallback checks
        key_regex = "^[A-Z]{2,5}-[0-9]{1,6}"
    match = re.search(key_regex, message)
    return match.group(0).upper() if match else None


def main() -> NoReturn:
    # Exit if the branch name does not contain a Jira issue key.
    git_branch_name = current_git_branch_name()
    print(git_branch_name)
    jira_issue_key = extract_jira_issue_key(git_branch_name)

    if not jira_issue_key:
        print("Jira not found in branch, searching for key in filenames...")
        files_changed = added_or_modified_filepaths()
        for filepath in files_changed:
            print(filepath)
            if jira_issue_key := extract_jira_issue_key(filepath, strict=True):
                break
    print(jira_issue_key)
    if not jira_issue_key:
        sys.exit(0)

    commit_msg_filepath = Path(sys.argv[1])
    commit_msg = commit_msg_filepath.read_text()

    # Exit if the commit message already contains a Jira issue key, even if it's
    # different from the one in the branch name.
    commit_first_line = commit_msg.splitlines()[0]
    if extract_jira_issue_key(commit_first_line):
        sys.exit(0)

    if jira_issue_key not in commit_first_line:
        commit_msg = f"[{jira_issue_key}] {commit_msg}"
        commit_msg_filepath.write_text(commit_msg)

    sys.exit(0)


if __name__ == "__main__":
    main()
