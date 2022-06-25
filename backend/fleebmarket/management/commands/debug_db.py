import djclick
from fleebmarket.utils.misc import ManagementLogging

ml = ManagementLogging()

from search_app.meilisearch_utils import MAdvertsItemsIndex
from search_app.models import RedditAdvertItem

logger = ml.getLogger()


@djclick.command()
def handle():
    advert_items_cli = MAdvertsItemsIndex.client()
    all_meili_ad_items = []
    offset = 0
    while res := advert_items_cli.get_documents({"offset": offset}):
        all_meili_ad_items.extend(res)
        offset += 20

    print(all_meili_ad_items[0].keys())
    pkeys = [item["pkey"] for item in all_meili_ad_items]
    print(len(set(pkeys)))

    db_items = RedditAdvertItem.objects.all()
    db_ids = [item.id for item in db_items]
    print(len(db_ids))

    print(len(set(pkeys) - set(db_ids)))

    all_search_res = []
    while True:
        res = advert_items_cli.search(
            "",
            {
                "offset": len(all_search_res),
                "limit": 9,
                "attributesToRetrieve": ["pkey", "sold"],
                "filter": None,
            },
        )
        if not res["hits"]:
            break
        print("Found", len(res["hits"]), len(all_search_res))
        all_search_res.extend(res["hits"])
        offset += len(res)
    print(len(all_search_res), len({item["pkey"] for item in all_search_res}))
