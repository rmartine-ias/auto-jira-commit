## Auto Jira commit

---

The original version has more features like time-tracking. See:
<https://github.com/radix-ai/auto-smart-commit>

---

This [pre-commit](https://pre-commit.com/) hook adds Jira keys to your Git
commit messages, if it can find them in the branch name. It doesn't add them if
a key already exists.

On a branch like `ABC-123`, `ABC-123-feature-name`, or `feature-abc-123`:

| Command | Log entry |
| ------- | --------- |
| `git commit -m "Release the kraken"` | [ABC-123] Release the kraken |
| `git commit -m "ABC-123 Release the kraken"` | ABC-123 Release the kraken |
| `git commit -m "[ABC-123] Release the kraken"` | [ABC-123] Release the kraken |
| `git commit -m "[DEF-456] Release the kraken"` | [DEF-456] Release the kraken |

If the branch name does not contain a Jira issue key, the commit message is not
modified.

See [How to Write a Git Commit
Message](https://chris.beams.io/posts/git-commit/) for an explanation of the
seven rules of a great Git commit message:

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line (automated)
4. Do not end the subject line with a period (automated)
5. Use the imperative mood in the subject line
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

## Installation

Add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/rmartine-ias/auto-jira-commit
    rev: v1.0
    hooks:
      - id: auto-jira-commit
```

and make sure to run `pre-commit install --hook-type prepare-commit-msg` to
install the hook type necessary for this hook.
