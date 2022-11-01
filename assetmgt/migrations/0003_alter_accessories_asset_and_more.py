# Generated by Django 4.1.1 on 2022-10-06 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assetmgt", "0002_assettype_alter_assetmodel_type_of_asset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accessories",
            name="asset",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="asset",
                to="assetmgt.assetmodel",
                verbose_name="Of Asset",
            ),
        ),
        migrations.AlterField(
            model_name="assetmodel",
            name="type_of_asset",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="assettype",
                to="assetmgt.assettype",
                verbose_name="Asset Type",
            ),
        ),
    ]