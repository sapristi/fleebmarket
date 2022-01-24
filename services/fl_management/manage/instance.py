import os
from subprocess import run
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
import time

from typer import style, colors
import humanize

from .git_info import get_git_info, GitRepoInfo
from .utils import log_command_res, run_command

def bgcolor(name):
    if "blue" in name:
        return name.replace("blue", style("blue", fg=colors.BLUE))
    if "green" in name:
        return name.replace("green", style("green", fg=colors.GREEN))
    return name

class HealthStatus(Enum):
    HEALTHY = style("HEALTHY", fg=colors.GREEN, bold=True)
    UNHEALTHY = style("UNHEALTHY", fg=colors.RED, bold=True)
    UNKNOWN = style("UNKNOWN", fg=colors.YELLOW, bold=True)


@dataclass
class ServiceStatus:
    name: str
    should_be_running: bool
    safe_delta_s: int
    running: bool
    running_since: Optional[timedelta]
    n_restarts: int

    @property
    def health_status(self) -> HealthStatus:
        """Checks that a service is healthy:

        If the service has restarted more than once per hour, then it is not healthy.

        If the service has been running for less than `self.safe_delta_s` seconds
        (and has not restarted), then we don't know.

        Otherwise it is healthy.
        """

        if not self.running:
            return HealthStatus.UNHEALTHY if self.should_be_running else HealthStatus.HEALTHY

        # if more than one restart per hour
        if self.n_restarts > self.running_since / timedelta(hours=1):
            return HealthStatus.UNHEALTHY

        if self.running_since < timedelta(seconds=self.safe_delta_s):
            return HealthStatus.UNKNOWN

        return HealthStatus.HEALTHY

    @property
    def errors(self):
        errors = []
        if self.should_be_running != self.running:
            if self.should_be_running:
                errors.append(f"not running")
            else:
                errors.append(f"running")
        if (status := self.health_status) != HealthStatus.HEALTHY:
            errors.append(f"{status}")
        return [(self.name, error) for error in errors]

    def format_terminal(self):
        status_str = style(
            "RUNNING" if self.running else "STOPPED",
            fg=colors.GREEN if (self.should_be_running == self.running) else colors.RED,
            bold=True
        ) + '/' + self.health_status.value

        running_since_str = ""
        if running_since := self.running_since:
            delta = humanize.naturaldelta(running_since, minimum_unit="milliseconds")
            running_since_str = f"(Running since {delta})"
        restarts_str = f"({self.n_restarts} restarts)"
        return f"{bgcolor(self.name):<25} : {status_str:<45} {running_since_str:<25} {restarts_str}"

@dataclass(unsafe_hash=True)
class Service:
    name: str
    should_be_running: bool
    safe_delta_s: int = 5

    def start(self):
        self.ctl("start")

    def stop(self):
        self.ctl("stop")

    def make_command(self, action, *args):
        return ['systemctl', '--user', action, self.name, *args]

    def ctl(self, action, *args, check=True):
        command = self.make_command(action, *args)
        return run_command(command, check)

    @property
    def running(self) -> bool:
        command = self.make_command("check")
        check_res = run_command(command, check=False)
        if check_res.returncode == 0:
            return True
        elif check_res.returncode == 3:
            return False
        else:
            log_command_res(command, check_res)
            check_res.check_returncode()
            return False # useless but makes type checking happy

    @property
    def running_since(self) -> Optional[timedelta]:
        if not self.running:
            return None
        res = self.ctl("show", "-P", "ActiveEnterTimestamp", check=True)
        timestamp = res.stdout.decode().strip()
        if not timestamp:
            return None
        running_since_abs = datetime.strptime(timestamp, "%a %Y-%m-%d %H:%M:%S %Z")
        return datetime.now() - running_since_abs

    @property
    def n_restarts(self) -> int:
        res = self.ctl("show", "-P", "NRestarts", check=True)
        return int(res.stdout)

    def get_status(self, wait):
        if wait and self.running_since is not None:
            running_since_s = self.running_since.total_seconds()
            if running_since_s < self.safe_delta_s:
                to_sleep = self.safe_delta_s - running_since_s + 1
                print(f"Waiting {int(to_sleep)}s for the service to become stable...")
                time.sleep(
                    to_sleep
                )
        return ServiceStatus(
            self.name,
            self.should_be_running,
            self.safe_delta_s,
            self.running,
            self.running_since,
            self.n_restarts
        )


@dataclass
class Instance:
    name: str
    is_main: bool
    repo_info: GitRepoInfo
    backend: Service
    cronjobs: Service

    @staticmethod
    def get_main():
        name = os.readlink(f'/etc/nginx/conf-bg/main')
        return Instance.get(name, True)

    @staticmethod
    def get_aux():
        name = os.readlink(f'/etc/nginx/conf-bg/aux')
        return Instance.get(name, False)

    @staticmethod
    def get(name: str, is_main: bool):
        repo_info = get_git_info(f"/fleebmarket_{name}")
        backend = Service(f"backend@{name}", should_be_running=True)
        cronjobs = Service(f"cronjobs@{name}", should_be_running=is_main)
        return Instance(name, is_main, repo_info, backend, cronjobs)

    @property
    def desc(self):
        return "Main" if self.is_main else "Aux"

    def collect_status(self, wait=False):
        self.backend_status = self.backend.get_status(wait)
        self.cronjobs_status = self.cronjobs.get_status(wait)

    def clear_status(self):
        self.backend_status = None
        self.cronjobs_status = None

    def errors(self):
        if self.backend_status is None or self.cronjobs_status is None:
            raise Exception("Status not collected")
        return [
            *self.backend_status.errors,
            *self.cronjobs_status.errors
        ]

    def format_terminal(self):
        if self.backend_status is None or self.cronjobs_status is None:
            raise Exception("Status not collected")
        return (
            style(f"{self.desc} instance: ", fg=colors.BRIGHT_WHITE) + bgcolor(self.name) + "\n"
            + self.repo_info.format_head_info() + "\n"
            f" - {'git status':<17}: {self.repo_info.format_status()}" "\n"
            f" - {self.backend_status.format_terminal()}" "\n"
            f" - {self.cronjobs_status.format_terminal()}"
        )
