import os
import typer
from cysystemd import journal
from .instance import Instance
from .utils import run_command

app = typer.Typer(no_args_is_help=True, help="manage fleebmarket services")

def print_journal(message):
    print(message)
    journal.send(
        message=message,
        priority=journal.Priority.INFO,
        syslog_identifier="fl_manage"
    )

def display_status(main_instance, aux_instance, wait=False):

    main_instance.collect_status(wait)
    aux_instance.collect_status(wait)

    print(main_instance.format_terminal())
    print()
    print(aux_instance.format_terminal())

    errors = [
        *main_instance.errors(),
        *aux_instance.errors()
    ]
    if errors:
        typer.secho("\nERRORS:", fg=typer.colors.RED, bold=True)
        for error in errors:
            typer.secho(f" - {error}", fg=typer.colors.RED)
    return errors

@app.command(help="display current status")
def status(
    wait: bool = typer.Option(False, help="Wait for instances to become stable")
):
    main_instance = Instance.get_main()
    aux_instance = Instance.get_aux()
    display_status(main_instance, aux_instance, wait)

@app.command(help="reset to the blue instance")
def reset():
    main_instance = Instance.get_main()
    aux_instance = Instance.get_aux()
    display_status(main_instance, aux_instance)

    print("\nNow resetting services...\n")

    main_instance.backend.start()
    main_instance.cronjobs.start()
    aux_instance.backend.start()
    aux_instance.cronjobs.stop()

    print("Reset done\n")

    display_status(main_instance, aux_instance, wait=True)

@app.command(help="restarts the aux backend")
def restart_aux_backend():
    aux_instance = Instance.get_aux()
    aux_instance.collect_status()
    print(aux_instance.format_terminal())

    print("\nNow restarting aux backend...\n")

    aux_instance.backend.ctl("restart")

    print("restarted\n")
    aux_instance.collect_status()
    print(aux_instance.format_terminal())

@app.command(help="swap between green and blue instances")
def swap(force: bool=False):
    main_instance = Instance.get_main()
    aux_instance = Instance.get_aux()
    errors = display_status(main_instance, aux_instance)

    print()
    print()
    if errors:
        if force:
            print("Warning: some services are in error, forcing swap nonetheless")
        else:
            print("Cannot swap: there are errors")
            return

    if not aux_instance.repo_info.is_clean():
        if force:
            print("Warning: aux repo not clean, forcing swap nonetheless")
        else:
            print("Cannot swap: aux git repo is not clean")
            return

    print("WARNING: if you made changes to the frontend, you will need to run")
    print(" - yarn build")
    print(" - python manage.py collectstatic")
    print("in order for your changes to take effect")
    print()
    input("Press a key to continue")

    print_journal("Swapping instances...")
    main_instance.cronjobs.stop()
    os.chdir("/etc/nginx/conf-bg")
    os.remove("main")
    os.remove("aux")
    os.symlink(f"{aux_instance.name}", "main")
    os.symlink(f"{main_instance.name}", "aux")
    aux_instance.cronjobs.start()
    run_command(['sudo', 'nginx', '-s', 'reload'], True)

    print_journal("Swap done.")
    print()
    main_instance = Instance.get_main()
    aux_instance = Instance.get_aux()
    display_status(main_instance, aux_instance, wait=True)
    print_journal(f"Main instance is now {main_instance.name}")
