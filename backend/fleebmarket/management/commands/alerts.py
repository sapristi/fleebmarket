import os

import djclick
from fleebmarket.utils.alerts import send, show


@djclick.group()
def group():
    """Collect alerts."""
    pass


def reduce_decorators(decorators, target_fn):
    if len(decorators):
        return decorators[0](reduce_decorators(decorators[1:], target_fn))
    else:
        return target_fn


reduce_decorators(
    [group.command(), djclick.option("--since-hours", type=int, default=1)], show
)

reduce_decorators(
    [
        group.command(),
        djclick.option(
            "--discord-token", default=lambda: os.environ.get("DISCORD_BOT_TOKEN")
        ),
        djclick.option("--test-channel", is_flag=True, help="Use test channel."),
        djclick.option("--since-hours", type=int, default=1),
    ],
    send,
)
