# Generated by Django 3.2.2 on 2021-05-09 18:59

import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FirstSurveyData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "trade_frequency",
                    models.CharField(
                        choices=[
                            ("never", "Never"),
                            ("yearly", "Once or twice a year"),
                            ("monthly", "Once or twice a month"),
                            ("many", "Many times a month"),
                        ],
                        max_length=100,
                    ),
                ),
                ("most_used_service", models.CharField(blank=True, max_length=100)),
                (
                    "most_traded_parts",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("full", "Full keyboards"),
                            ("keysets", "Keysets"),
                            ("keycaps", "Keycaps (including artisan)"),
                            ("switches", "Switches"),
                            ("other", "Other parts"),
                        ],
                        max_length=35,
                    ),
                ),
                (
                    "service_interest",
                    models.CharField(
                        choices=[
                            ("yes", "Yes"),
                            ("maybe", "Maybe"),
                            ("no", "No"),
                            ("other", "I don't know"),
                        ],
                        max_length=100,
                    ),
                ),
                ("essential_features", models.CharField(blank=True, max_length=10000)),
                ("missed_features", models.CharField(blank=True, max_length=10000)),
                (
                    "would_pay",
                    models.CharField(
                        choices=[
                            ("yes", "Yes"),
                            ("maybe", "Maybe"),
                            ("no", "No"),
                            ("other", "I don't know"),
                        ],
                        max_length=100,
                    ),
                ),
                ("paying_features", models.CharField(blank=True, max_length=10000)),
                ("how_many_keebs", models.PositiveIntegerField()),
                (
                    "like_fleebmarket",
                    models.CharField(
                        choices=[
                            ("yesyes", "I love it"),
                            ("yes", "It's ok"),
                            ("no", "It sucks"),
                            ("other", "I don't care"),
                        ],
                        max_length=100,
                    ),
                ),
                ("anything_else", models.CharField(blank=True, max_length=10000)),
                ("current_year", models.PositiveIntegerField()),
            ],
        ),
    ]
