import praw
import requests
from django.conf import settings


class RedditClient:
    _instance = None

    def __init__(self):
        if RedditClient._instance is None:
            RedditClient._instance = praw.Reddit(**settings.REDDIT_BOT_CREDS)
        self.instance = RedditClient._instance

    def send_message(self, user_id, title, message):
        reddit_user = self.instance.redditor(name=user_id)
        reddit_user.message(title, message)


class DiscordClient:
    def __init__(self):
        token = settings.DISCORD_CREDS["bot_token"]
        self.headers = {"Authorization": f"Bot {token}"}

    def send_message(self, user_id, message):
        resp = requests.post(
            "https://discord.com/api/users/@me/channels",
            json={"recipient_id": user_id},
            headers=self.headers,
        )
        print("channel", resp.json())
        channel_id = resp.json()["id"]
        resp = requests.post(
            f"https://discord.com/api/channels/{channel_id}/messages",
            json={"content": message},
            headers=self.headers,
        )
        print("message", resp.json())
