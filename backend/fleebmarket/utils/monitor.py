import re
import socket
from datetime import datetime, timedelta

from cysystemd.reader import JournalOpenMode, JournalReader, Rule


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


def show(
    since_hours: int,
):
    """Print stats to stdout."""
    since = datetime.now() - timedelta(hours=since_hours, minutes=5)
    reader = collect_journal_messages(since)
    data = compute_data(reader)
    print(data)


def put():
    """Send stats to graphene collector."""
    now = datetime.now()
    hourly_data = collect_data(now, 1)
    daily_data = collect_data(now, 24)
    weekly_data = collect_data(now, 168)

    addr = ("127.0.0.1", 2003)
    ts = int(now.timestamp())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(addr)
        data = b""
        data += f"usage.hourly.total {hourly_data['nb_total']} {ts}\n".encode()
        data += f"usage.hourly.distinct {hourly_data['nb_distinct']} {ts}\n".encode()

        data += f"usage.daily.total {daily_data['nb_total']} {ts}\n".encode()
        data += f"usage.daily.distinct {daily_data['nb_distinct']} {ts}\n".encode()

        data += f"usage.weekly.total {weekly_data['nb_total']} {ts}\n".encode()
        data += f"usage.weekly.distinct {weekly_data['nb_distinct']} {ts}\n".encode()
        s.sendall(data)
    print("Sent data")
