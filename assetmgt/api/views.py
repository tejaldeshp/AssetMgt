from assetmgt.models import AssetModel, Accessories, AssetType
from assetmgt.api.serializers import (
    AssetSerializer,
    AccessorySerializer,
    AssetTypeSerializer,
)
from rest_framework import viewsets


class AssetViewSet(viewsets.ModelViewSet):
    queryset = AssetModel.objects.all()
    serializer_class = AssetSerializer


class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessories.objects.all()
    serializer_class = AccessorySerializer


class AssetTypeViewSet(viewsets.ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer
