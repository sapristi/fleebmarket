import os
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from blessings import Terminal
from cysystemd.reader import JournalEntry, JournalOpenMode, JournalReader, Rule
from fleebmarket.management.utils import Instance

t = Terminal()


@dataclass(unsafe_hash=True)
class AlertEntry:
    message: str
    service: str
    level: int

    def format_terminal(self, count) -> str:
        return t.bold(f"[{self.service}]: {count} occurences\n") + self.message

    def format_discord(self, count) -> str:
        return f"**[{self.service}]: {count} occurences**:\n{self.message}"

    @staticmethod
    def from_journal_entry(entry: JournalEntry):
        return AlertEntry(
            message=entry.data["MESSAGE"],
            service=entry.data["SYSLOG_IDENTIFIER"],
            level=entry.data["PRIORITY"],
        )


class AlertsCollector:
    @staticmethod
    def load_lines(path: Path):
        if path.is_file():
            with open(path) as f:
                return [word for word in f.read().split() if word]
        else:
            print("Warning: cannot load lines from file", path)
            return []

    def __init__(self):
        services_ignored_file = (
            Path(os.environ["DATA_PATH"]) / "alerts" / "services_ignored"
        )
        messages_ignored_file = (
            Path(os.environ["DATA_PATH"]) / "alerts" / "messages_ignored"
        )
        self.services_ignored = self.load_lines(services_ignored_file)
        self.messages_ignored = self.load_lines(messages_ignored_file)

        self.alerts: Counter[AlertEntry] = Counter()

    def is_entry_ignored(self, entry: AlertEntry):
        return entry.service in self.services_ignored or any(
            (message_ignored in entry.message)
            for message_ignored in self.messages_ignored
        )

    def collect_journal_messages(
        self, since: datetime, journal_mode: JournalOpenMode, rule: Rule
    ):
        reader = JournalReader()
        reader.open(journal_mode)
        reader.seek_realtime_usec(since.timestamp() * 1000000)
        reader.add_filter(rule)

        self.alerts.update(
            AlertEntry.from_journal_entry(entry)
            for entry in reader
            if not self.is_entry_ignored(AlertEntry.from_journal_entry(entry))
        )

    def collect_services_alerts(
        self,
    ):
        main_instance = Instance.get_main()
        aux_instance = Instance.get_aux()

        main_instance.collect_status(wait=True)
        aux_instance.collect_status(wait=True)

        errors = [*main_instance.errors(), *aux_instance.errors()]
        self.alerts.update(
            (AlertEntry(message, service, 3) for (service, message) in errors)
        )

    def collect_all(
        self,
        since_hours: int,
    ):
        since = datetime.now() - timedelta(hours=since_hours, minutes=5)
        print("Fetching errors since", since)
        rule = Rule("PRIORITY", "3") | Rule("PRIORITY", "2") | Rule("PRIORITY", "1")
        self.collect_journal_messages(since, JournalOpenMode.SYSTEM, rule)
        self.collect_journal_messages(since, JournalOpenMode.CURRENT_USER, rule)

        self.collect_services_alerts()


def show(since_hours: int):
    """Print collected alerts to stdout."""
    collector = AlertsCollector()
    collector.collect_all(since_hours)
    if len(collector.alerts) == 0:
        print("No error")
        return

    for alert, count in collector.alerts.most_common():
        print(alert.format_terminal(count))


def send(
    discord_token: str,
    test_channel: bool,
    since_hours: int,
):
    """Send collected alters to the discord #alerts channel."""
    import requests  # delayed import for performance

    channel_id = 908122255417020458 if test_channel else 906427494561894421
    collector = AlertsCollector()
    collector.collect_all(since_hours)
    if len(collector.alerts) == 0:
        print("No error")
        return

    print(f"Found {len(collector.alerts)} errors.")
    for alert, count in collector.alerts.most_common():
        content_trunc = alert.format_discord(count)[:2000]
        response = requests.post(
            f"https://discord.com/api/channels/{channel_id}/messages",
            headers={"Authorization": f"Bot {discord_token}"},
            json={"content": content_trunc},
        )
        try:
            response.raise_for_status()
        except Exception:
            print("Failed sending alert:", response.text)
            print(response.text)
