from subprocess import run
from typer import style, colors


def log_command_res(command, command_res):
    if command_res.returncode != 0:
        print(
            style("ERROR", fg=colors.RED, bold=True),
            "running",
            style(" ".join(command), fg=colors.BLUE)
        )
    else:
        print(
            style(" ".join(command), fg=colors.BLUE),
            "executed successfuly"
        )
    print("Captured:")
    print("stdout", command_res.stdout)
    print("stdout", command_res.stderr)
    print()


def run_command(command, check):
    res = run(command, capture_output=True)
    if check and res.returncode != 0:
        log_command_res(command, res)
        res.check_returncode()
    return res
