from dataclasses import dataclass
from datetime import datetime

from blessings import Terminal
from git.repo import Repo

t = Terminal()


@dataclass
class GitCommit:
    author: str
    message: str
    datetime: datetime

    def __repr__(self):
        author = t.bright_black(self.author)
        message = t.bright_black(self.message)
        datetime = t.bright_black(str(self.datetime))
        return f"{message} by {author} at {datetime}"


@dataclass
class GitRepoInfo:
    branch_name: str
    unstaged_changes: int
    staged_changes: int
    untracked_files: int
    commit: GitCommit

    def is_clean(self):
        return self.staged_changes + self.unstaged_changes + self.untracked_files == 0

    def format_head_info(self):
        branch_name = t.magenta(f" {self.branch_name}")
        return f"{branch_name} - {self.commit}"

    def format_status(self):
        if self.is_clean():
            return t.bold_green("CLEAN")
        else:
            status = t.bold_red("DIRTY")
            details = []
            if self.staged_changes:
                details.append(f"{self.staged_changes} staged")
            if self.unstaged_changes:
                details.append(f"{self.unstaged_changes} unstaged")
            if self.untracked_files:
                details.append(f"{self.untracked_files} untracked")

            status_detail = "(" + ",".join(details) + ")"
            return f"{status:<32} {status_detail}"


def get_git_info(path):
    repo = Repo(path)
    commit = repo.commit()
    last_commit = GitCommit(
        commit.author.name, commit.message.strip(" \n"), commit.committed_datetime  # type: ignore
    )
    return GitRepoInfo(
        repo.active_branch.name,
        len(repo.index.diff(None)),
        len(repo.index.diff(repo.head.commit)),
        len(repo.untracked_files),
        last_commit,
    )
