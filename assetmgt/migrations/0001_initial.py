# Generated by Django 4.1.1 on 2022-09-26 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dtm_created",
                    models.DateTimeField(auto_now_add=True, verbose_name="DTM Created"),
                ),
                (
                    "dtm_updated",
                    models.DateTimeField(auto_now=True, verbose_name="DTM Updated"),
                ),
                ("model_id", models.CharField(max_length=20, verbose_name="Model ID")),
                ("brand_name", models.CharField(max_length=15, verbose_name="Brand")),
                (
                    "type_of_asset",
                    models.CharField(
                        choices=[
                            ("CPU", "CPU"),
                            ("Keyboard", "Keyboard"),
                            ("Mouse", "Mouse"),
                            ("Monitor", "Monitor"),
                        ],
                        max_length=30,
                        verbose_name="Type",
                    ),
                ),
                ("date_procured", models.DateField(verbose_name="Date Procured")),
                ("price", models.FloatField(verbose_name="Price")),
                (
                    "date_allotted",
                    models.DateField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Date Allotted",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Accessories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dtm_created",
                    models.DateTimeField(auto_now_add=True, verbose_name="DTM Created"),
                ),
                (
                    "dtm_updated",
                    models.DateTimeField(auto_now=True, verbose_name="DTM Updated"),
                ),
                ("model_id", models.CharField(max_length=30, verbose_name="Model ID")),
                (
                    "accessory_type",
                    models.CharField(max_length=20, verbose_name="Type"),
                ),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assetmgt.assetmodel",
                        verbose_name="Of Asset",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]