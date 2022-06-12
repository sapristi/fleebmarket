import re
import socket
from datetime import datetime, timedelta

import djclick
from cysystemd.reader import JournalOpenMode, JournalReader, Rule
from fleebmarket.utils import monitor


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

        match = re.match("\w+: +(?P<ip>.*?):0 - .*", msg)
        ip = match.group("ip")
        ips.add(ip)
        nb_total += 1

    return {"nb_total": nb_total, "nb_distinct": len(ips)}


def collect_data(now, since_hours: int):
    since = now - timedelta(hours=since_hours, minutes=5)
    reader = collect_journal_messages(since)
    return compute_data(reader)


@djclick.group()
def group():
    """Collect alerts."""
    pass


@group.command()
@djclick.option("--since-hours", type=int, default=1)
def show(
    since_hours: int,
):
    """Print stats to stdout."""
    stats = monitor.get(since_hours)
    print(stats)


@group.command()
def put():
    """Send stats to graphene collector."""
    monitor.put()

@group.command()
def put_to_disk():
    """Save stats to files in /tmp."""
    monitor.put_to_disk()
