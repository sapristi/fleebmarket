from subprocess import run

from blessings import Terminal

t = Terminal()


def log_command_res(command, command_res):
    if command_res.returncode != 0:
        print(
            t.bold_red("ERROR"),
            "running",
            t.blue(" ".join(command)),
        )
    else:
        print(t.blue(" ".join(command)), "executed successfuly")
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
