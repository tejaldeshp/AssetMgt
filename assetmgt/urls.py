from django.urls import path
from assetmgt.views import *
from . import views

app_name = "assetmgt"
urlpatterns = [
    path("assets/", AssetView.as_view(), name="assetlist"),
    path("assets/add/", AssetCreateView.as_view(), name="add"),
    path("assets/<int:pk>/", AssetUpdateView.as_view(), name="update"),
    path("assets/<int:pk>/delete/", AssetDeleteView.as_view(), name="delete"),
    path("accessories/", AccessoriesView.as_view(), name="accessorylist"),
    path(
        "accessories/detail/<int:pk>/",
        AccessoryDetail.as_view(),
        name="accessorydetail",
    ),
    path("accessories/add/", AccessoryCreateView.as_view(), name="acc_add"),
    path("accessories/<int:pk>/", AccessoryUpdateView.as_view(), name="acc_update"),
    path(
        "accessories/<int:pk>/delete/", AccessoryDeleteView.as_view(), name="acc_delete"
    ),
    path("accassets/<int:pk>/", AccAsset.as_view(), name="acc_asset"),
    path("<int:pk>/", AssetDetail.as_view(), name="assetdetail"),
]
