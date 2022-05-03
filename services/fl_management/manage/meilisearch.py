import typer
import os
from collections import Counter
app = typer.Typer(help="View meilisearch status", no_args_is_help=True)

INDICES = ["Adverts", "AdvertItems"]

def get_tasks_status(icli):
    tasks = icli.get_tasks()
    tasks_count = Counter((task["status"] for task in tasks["results"]))
    return tasks_count.most_common()


@app.command()
def status():
    import meilisearch
    import pprint

    client = meilisearch.Client(os.environ['MEILISEARCH_HOST'], timeout=5)

    for index in INDICES:
        print("Index", index)
        icli = client.index(index)
        print("Tasks:")
        pprint.pprint(get_tasks_status(icli))

        print()
        print("Settings:")
        settings = icli.get_settings()
        settings["stopWords"] = len(settings.get("stopWords", []))
        pprint.pprint(settings)
        print()

        print("Stats")
        stats = icli.get_stats()
        pprint.pprint(stats)

        print()
        print()
