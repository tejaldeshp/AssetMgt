from django.urls import path, include
from assetmgt.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("asset", views.AssetViewSet, basename="asset")
router.register("accessory", views.AccessoryViewSet, basename="accessory")
router.register("assettype", views.AssetTypeViewSet, basename="assettype")

urlpatterns = [path("", include(router.urls))]
