import logging
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount

from fleebmarket.connectors import RedditClient, DiscordClient

logger = logging.getLogger(__name__)

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('accounts:edit-profile', kwargs={'pk': self.pk})

    def send_message(self, title, message):
        social_accounts = SocialAccount.objects.filter(user = self).all()

        for account in social_accounts:
            try:
                if account.provider == "reddit":
                    RedditClient().send_message(account.uid, title, message)
                if account.provider == "discord":
                    DiscordClient().send_message(account.uid, message)
            except Exception as exc:
                logger.error("Sending of message to [%s] failed (%s, %s) (%s)", account.uid, title, message, exc)
