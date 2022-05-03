import djclick
import pprint
from collections import Counter
from search_app.meilisearch_utils import MAdvertsIndex, MAdvertsItemsIndex
from search_app.models import RedditAdvert, RedditAdvertItem

def get_tasks_status(icli):
    tasks = icli.get_tasks()
    tasks_count = Counter((task["status"] for task in tasks["results"]))
    return tasks_count.most_common()


@djclick.command()
def command():

    for index in (MAdvertsIndex, MAdvertsItemsIndex):
        print("Index", index.name)
        icli = index.client()
        print("Tasks:")
        pprint.pprint(get_tasks_status(icli))

        print()
        print("Settings:")
        settings = icli.get_settings()
        settings["stopWords"] = len(settings.get("stopWords", []))
        pprint.pprint(settings)
        print()

        print("Stats:")
        stats = icli.get_stats()
        pprint.pprint(stats)

        print()
        print()

    for model in (RedditAdvert, RedditAdvertItem):
        print("Table", model.__name__)
        count = model.objects.count()
        print("Count", count)
        print()
