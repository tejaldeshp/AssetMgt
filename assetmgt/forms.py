from django.forms import ModelForm
from assetmgt.models import Accessories, AssetModel
from django import forms


class AccessoryForm(ModelForm):
    class Meta:
        model = Accessories
        fields = ["model_id", "accessory_type"]


class DateInput(forms.DateInput):
    input_type = "date"


class AssetForm(ModelForm):
    class Meta:
        model = AssetModel
        fields = "__all__"
        widgets = {
            "date_procured": DateInput(),
            "date_allotted": DateInput(),
        }
