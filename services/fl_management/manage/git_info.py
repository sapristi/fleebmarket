from datetime import datetime
from typer import style, colors
from git.repo import Repo
from dataclasses import dataclass


@dataclass
class GitCommit:
    author: str
    message: str
    datetime: datetime

    def __repr__(self):
        author = style(self.author, fg=colors.BRIGHT_BLACK)
        message = style(self.message, fg=colors.BRIGHT_BLACK)
        datetime = style(str(self.datetime), fg=colors.BRIGHT_BLACK)
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
        branch_name = style(f" {self.branch_name}", fg=colors.MAGENTA)
        return f"{branch_name} - {self.commit}"

    def format_status(self):
        if self.is_clean():
            return style("CLEAN", fg=colors.GREEN, bold=True)
        else:
            status = style("DIRTY", fg=colors.RED, bold=True)
            details = []
            if self.staged_changes:
                details.append(style(f"{self.staged_changes} staged" ))
            if self.unstaged_changes:
                details.append(style(f"{self.unstaged_changes} unstaged"))
            if self.untracked_files:
                details.append(style(f"{self.untracked_files} untracked"))

            status_detail = "(" + ",".join(details) + ")"
            return f"{status:<32} {status_detail}"


def get_git_info(path):
    repo =  Repo(path)
    commit = repo.commit()
    last_commit = GitCommit(
        commit.author.name,
        commit.message.strip(" \n"),
        commit.committed_datetime
    )
    return GitRepoInfo(
        repo.active_branch.name,
        len(repo.index.diff(None)),
        len(repo.index.diff(repo.head.commit)),
        len(repo.untracked_files),
        last_commit
    )
