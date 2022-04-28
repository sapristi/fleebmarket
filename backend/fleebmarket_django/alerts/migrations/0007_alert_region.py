# Generated by Django 3.2.2 on 2021-08-25 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0006_alert_ad_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="alert",
            name="region",
            field=models.CharField(
                choices=[
                    ("EU", "EU"),
                    ("US", "US"),
                    ("CA", "CA"),
                    ("OTHER", "OTHER"),
                    ("Any", "Any"),
                ],
                default="Any",
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]
