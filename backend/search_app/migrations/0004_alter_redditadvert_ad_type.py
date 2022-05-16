# Generated by Django 3.2.2 on 2021-08-19 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("search_app", "0003_alter_redditadvert_ad_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="redditadvert",
            name="ad_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Selling", "Selling"),
                    ("Buying", "Buying"),
                    ("Trading", "Trading"),
                    ("Traded", "Traded"),
                    ("Sold", "Sold"),
                    ("Purchased", "Purchased"),
                    ("Artisan", "Artisan"),
                    ("Bulk", "Bulk"),
                    ("Interest_check", "Interest Check"),
                    ("Vendor", "Vendor"),
                    ("Group_buy", "Group Buy"),
                    ("Service", "Service"),
                    ("Meta", "Meta"),
                    ("Giveaway", "Giveaway"),
                    ("Any", "Any"),
                ],
                db_index=True,
                max_length=20,
                null=True,
            ),
        ),
    ]