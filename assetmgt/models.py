from django.db import models
from qux.models import CoreModel
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.models import User


class AssetType(CoreModel):
    name = models.CharField(max_length=20, verbose_name="Asset Type")

    def __str__(self):
        return self.name


class AssetModel(CoreModel):
    model_id = models.CharField(max_length=20, verbose_name="Model ID")
    brand_name = models.CharField(max_length=15, verbose_name="Brand")
    type_of_asset = models.ForeignKey(
        AssetType,
        on_delete=models.DO_NOTHING,
        verbose_name="Asset Type",
        related_name="assettype",
    )
    date_procured = models.DateField(verbose_name="Date Procured")
    price = models.FloatField(verbose_name="Price")
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        default=None,
        blank=True,
        verbose_name="User",
    )
    date_allotted = models.DateField(
        null=True, default=None, verbose_name="Date Allotted", blank=True
    )

    def __str__(self):
        return str(self.id) + self.type_of_asset.name

    def get_absolute_url(self):
        # return reverse("assetmgt:assetdetail", kwargs={"pk": self.pk})
        return reverse("assetmgt:all_assets")


class Accessories(CoreModel):
    model_id = models.CharField(max_length=30, verbose_name="Model ID")
    accessory_type = models.CharField(max_length=20, verbose_name="Type")
    asset = models.ForeignKey(
        AssetModel,
        on_delete=models.CASCADE,
        verbose_name="Of Asset",
        related_name="accessory",
    )

    def __str__(self):
        return self.accessory_type

    def get_absolute_url(self):
        return reverse("assetmgt:accessorydetail", kwargs={"pk": self.pk})


# class AssetForm(ModelForm):
#     class Meta:
#         model = AssetModel
#         fields = "__all__"
