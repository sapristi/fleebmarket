import subprocess

import djclick
from django.conf import settings
from django.core.management import call_command
from utils import ManagementLogging

ml = ManagementLogging()

logger = ml.getLogger()


@djclick.command()
@djclick.pass_verbosity
def handle(verbosity):
    ml.set_level_from_verbosity(verbosity)

    frontend_dir = settings.ROOT_DIR / ".." / "frontend"
    subprocess.run(["pnpm", "build"], cwd=str(frontend_dir))
    call_command("collectstatic")
