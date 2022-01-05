from utils import ChoiceEnum

class RedditAdvertType(str, ChoiceEnum):
    Selling = "Selling"
    Buying = "Buying"
    Trading = 'Trading'
    Traded = 'Traded'
    Sold = "Sold"
    Purchased = "Purchased"
    Artisan = "Artisan"
    Bulk = "Bulk"
    Interest_check = "Interest Check"
    Vendor = "Vendor"
    Group_buy = "Group Buy"
    Service = "Service"
    Meta = "Meta"
    Giveaway = "Giveaway"
    Any = "Any"

    @staticmethod
    def ignored() -> list["RedditAdvertType"]:
        return [
            RedditAdvertType.Interest_check,
            RedditAdvertType.Vendor,
            RedditAdvertType.Group_buy,
            RedditAdvertType.Service,
            RedditAdvertType.Meta,
            RedditAdvertType.Giveaway,
            RedditAdvertType.Any,
        ]

