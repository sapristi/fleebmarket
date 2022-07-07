import djclick
from fleebmarket.utils import monitor


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
