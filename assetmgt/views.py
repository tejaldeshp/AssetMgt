from http.client import HTTPResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import AssetModel, Accessories, AssetType
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AccessoryForm, AssetForm

# view for all assets available can have specific type drop down to pick type to list
class AssetView(ListView):
    model = AssetModel
    template_name = "assetmgt/all_assets.html"

    def get_queryset(self):
        type = self.request.GET.get("type", None)
        if type == None or type == "All":
            queryset = super().get_queryset()
        else:
            queryset = AssetModel.objects.filter(type_of_asset__name=type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tup = [x.name for x in AssetType.objects.all()]
        context["assettype"] = tup
        return context


# view for specific asset and accessories attached to
class AssetDetail(DetailView):
    model = AssetModel
    template_name = "assetmgt/asset_detail.html"
    # handle selected from the list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = AssetModel._meta.fields
        context["fields"] = fields
        context["id"] = kwargs.get("id", None)
        return context

    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        querys = Accessories.objects.filter(asset=id)
        context = {}
        assetname = AssetModel.objects.get(pk=id)
        context["object"] = assetname
        context["acc_list"] = querys
        return render(request, self.template_name, context)


class AssetCreateView(CreateView):
    model = AssetModel
    form_class = AssetForm
    template_name = "assetmgt/addasset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assetform"] = context.pop("form")
        return context

    def post(self, request, *args, **kwargs):
        if "save_add" in request.POST:
            self.success_url = reverse("assetmgt:add")
        elif "acc_add" in request.POST:
            self.success_url = reverse("assetmgt:acc_add")
        else:
            self.success_url = reverse("assetmgt:assetlist")
        return super().post(request, *args, **kwargs)


class AssetUpdateView(UpdateView):
    model = AssetModel
    form_class = AssetForm
    template_name = "assetmgt/updateasset.html"

    def get_context_data(self, **kwargs):
        id = self.kwargs.get("pk", None)
        querys = Accessories.objects.filter(asset=id)
        kwargs["acc_list"] = querys
        kwargs["id"] = id
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("assetmgt:assetlist")


class AssetDeleteView(DeleteView):
    model = AssetModel
    success_url = reverse_lazy("assetmgt:assetlist")
    template_name = "assetmgt/deleteasset.html"

    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        querys = Accessories.objects.filter(asset=id)
        context = {}
        assetname = AssetModel.objects.get(pk=id)
        context["object"] = assetname
        context["acc_list"] = querys
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse("assetmgt:assetlist")


# Accessories Views


class AccessoriesView(ListView):
    model = Accessories
    template_name = "assetmgt/all_accessories.html"

    def get_queryset(self):
        id = self.request.GET.get("pk", None)
        qs = Accessories.objects.filter(asset=id)
        return qs


class AccessoryDetail(DetailView):
    model = Accessories
    template_name = "assetmgt/accessory_detail.html"


class AccessoryCreateView(LoginRequiredMixin, CreateView):
    model = Accessories
    template_name = "assetmgt/addaccessory.html"
    form_class = AccessoryForm
    asset = None

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.asset = self.asset
        self.object.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        id = request.GET.get("pk", None)
        if id:
            self.asset = AssetModel.objects.get(id=id)
        else:
            self.asset = AssetModel.objects.latest("id")
        return super().post(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     print(super().get_context_data(**kwargs))
    #     print("kwargs", kwargs)
    #     asset = AssetModel.objects.latest("id")
    #     print(asset)
    #     content = super().get_context_data(**kwargs)
    #     content["form"].initial["asset"] = asset
    #     # content["form"].fields["asset"].disabled = True
    #     print(content["form"].fields["asset"])
    #     return content

    def get_success_url(self):
        return reverse("assetmgt:assetlist")


class AccessoryUpdateView(UpdateView):
    model = Accessories
    template_name = "assetmgt/updateaccessory.html"
    form = AccessoryForm


class AccessoryDeleteView(DeleteView):
    model = Accessories
    success_url = reverse_lazy("assetmgt:assetlist")
    template_name = "assetmgt/deleteaccessory.html"


class AccAsset(ListView):
    model = Accessories
    template_name = "assetmgt/accasset.html"

    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        print(id)
        self.object_list = self.get_queryset()
        querys = Accessories.objects.filter(asset=id)
        context = {}
        assetname = AssetModel.objects.get(pk=id)
        context["asset"] = assetname
        context["object_list"] = querys
        print(context)
        return render(request, self.template_name, context)
