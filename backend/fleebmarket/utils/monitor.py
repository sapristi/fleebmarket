import re
import socket
from datetime import datetime, timedelta
from pathlib import Path

from cysystemd.reader import JournalOpenMode, JournalReader, Rule
from search_app.models import RedditAdvert, RedditAdvertType


def collect_journal_messages(
    since: datetime,
    # rule: Rule
):
    rule = Rule("SYSLOG_IDENTIFIER", "Backend[blue]") | Rule(
        "SYSLOG_IDENTIFIER", "Backend[green]"
    )
    reader = JournalReader()
    reader.open(JournalOpenMode.CURRENT_USER)
    reader.seek_realtime_usec(since.timestamp() * 1000000)
    reader.add_filter(rule)

    return reader


def compute_data(entries):
    ips = set()
    nb_total = 0
    for entry in entries:
        msg = entry.data["MESSAGE"]
        if not "GET /api/search/" in msg:
            continue
        if "208.115.199.25" in msg:
            continue

        match = re.match(r"(?P<ip>.*?) GET.*", msg)
        if not match:
            continue
        ip = match.group("ip")
        ips.add(ip)
        nb_total += 1

    return {"nb_total": nb_total, "nb_distinct": len(ips)}


def collect_data(now, since_hours: int):
    since = now - timedelta(hours=since_hours, minutes=5)
    reader = collect_journal_messages(since)
    return compute_data(reader)


def get(
    since_hours: int,
):
    """Print stats to stdout."""
    since = datetime.now() - timedelta(hours=since_hours, minutes=5)
    reader = collect_journal_messages(since)
    data = compute_data(reader)
    return data


def put_to_disk():
    """Save stats to files in /tmp."""
    dest = Path("/tmp/monitorix")
    dest.mkdir(exist_ok=True)
    now = datetime.now()
    to_collect = {"hourly": 1, "daily": 24, "weekly": 168}
    for period, nb_hours in to_collect.items():
        data = collect_data(now, nb_hours)
        with open(dest / f"{period}_distinct_ip", "w") as f:
            f.write(str(data["nb_distinct"]))
        with open(dest / f"{period}_total_ip", "w") as f:
            f.write(str(data["nb_total"]))
