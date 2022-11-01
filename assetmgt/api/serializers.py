from dataclasses import fields
from assetmgt.models import AssetModel, Accessories, AssetType
from rest_framework import serializers


class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessories
        fields = ["id", "model_id", "accessory_type", "asset"]


class AssetSerializer(serializers.ModelSerializer):
    accessory = AccessorySerializer(many=True, read_only=True)

    class Meta:
        model = AssetModel
        fields = [
            "id",
            "model_id",
            "brand_name",
            "type_of_asset",
            "date_procured",
            "price",
            "user",
            "date_allotted",
            "accessory",
        ]


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ["id", "name"]
