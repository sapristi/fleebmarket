import os

import djclick
from blessings import Terminal
from cysystemd import journal
from fleebmarket.management.utils import Instance, run_command

t = Terminal()


@djclick.group()
def group():
    """Manage systemd services."""
    pass


def print_journal(message):
    print(message)
    journal.send(
        message=message, priority=journal.Priority.INFO, syslog_identifier="fl_manage"
    )


def display_status(main_instance, aux_instance, wait=False):

    main_instance.collect_status(wait)
    aux_instance.collect_status(wait)

    print(main_instance.format_terminal())
    print()
    print(aux_instance.format_terminal())

    errors = [*main_instance.errors(), *aux_instance.errors()]
    if errors:
        print(t.bold_red("\nERRORS:"))
        for error in errors:
            print(t.red(f" - {error}"))
    return errors


@group.command()
@djclick.option("--wait", is_flag=True, help="Wait for instances to become stable")
def status(wait: bool):
    """Display current status."""
    main_instance = Instance.get_main()
    aux_instance = Instance.get_aux()
    display_status(main_instance, aux_instance, wait)


@group.command()
def reset():
    """Reset to the blue instance."""
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


@group.command()
def restart_aux_backend():
    """Restarts the aux backend."""
    aux_instance = Instance.get_aux()
    aux_instance.collect_status()
    print(aux_instance.format_terminal())

    print("\nNow restarting aux backend...\n")

    aux_instance.backend.ctl("restart")

    print("restarted\n")
    aux_instance.collect_status()
    print(aux_instance.format_terminal())


@group.command()
@djclick.option(
    "--force", is_flag=True, help="Swap even if some services are in error."
)
def swap(force: bool = False):
    """Swap between green and blue instances."""
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
    run_command(["sudo", "nginx", "-s", "reload"], True)

    print_journal("Swap done.")
    print()
    main_instance = Instance.get_main()
    aux_instance = Instance.get_aux()
    display_status(main_instance, aux_instance, wait=True)
    print_journal(f"Main instance is now {main_instance.name}")
