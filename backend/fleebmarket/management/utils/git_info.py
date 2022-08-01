import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from blessings import Terminal
from django.utils.timezone import now
from git.repo import Repo
from humanize import naturaldelta

logger = logging.getLogger(__name__)
t = Terminal()


@dataclass
class GitCommit:
    author: str
    message: str
    at: datetime

    def __repr__(self):
        author = t.bright_black(self.author)
        message = t.bright_blue(self.message)
        at = t.bright_blue(str(self.at))
        when = t.bright_blue(naturaldelta(now() - self.at))
        return f"{message} by {author} {when} ago"


@dataclass
class GitRepoInfo:
    branch_name: str
    unstaged_changes: int
    staged_changes: int
    untracked_files: int
    commit: GitCommit
    remote_status: Optional[Tuple[str, str]]

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

    def format_remote_status(self):
        if self.remote_status is None:
            return "No remote branch set"
        else:
            if self.remote_status == ("0", "0"):
                return "On par with remote"
            else:
                ahead, behind = self.remote_status
                res = ""
                if ahead != "0":
                    res += f"{t.bright_yellow(ahead)} commits ahead; "
                if behind != "0":
                    res += f"{t.bright_yellow(behind)} commits behind"
                return res


def get_git_info(path):
    repo = Repo(path)
    try:
        repo.remotes[0].fetch()
    except Exception as exc:
        logger.warning("Failed to fetch git remote (%s)", exc)
    commit = repo.commit()
    last_commit = GitCommit(
        commit.author.name, commit.message.strip(" \n"), commit.committed_datetime  # type: ignore
    )
    if repo.active_branch.tracking_branch() is None:
        remote_status = None
    else:
        ahead_behind = repo.git.execute(
            [
                "git",
                "rev-list",
                "--left-right",
                "--count",
                f"{repo.active_branch.name}...origin/{repo.active_branch.name}",
            ]
        )
        remote_status = tuple(ahead_behind.split("\t"))
    return GitRepoInfo(
        repo.active_branch.name,
        len(repo.index.diff(None)),
        len(repo.index.diff(repo.head.commit)),
        len(repo.untracked_files),
        last_commit,
        remote_status,
    )
