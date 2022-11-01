from itertools import chain

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.utils import timezone
from django.utils.crypto import get_random_string
from rangefilter.filters import DateRangeFilter
from django.core.exceptions import FieldError

default_null_blank = dict(default=None, null=True, blank=True)


def qux_model_to_dict(
    instance,
    fields=None,
    exclude=None,
    exclude_none=False,
    verbose_name=False,
):
    if exclude is None:
        exclude = ["id", "dtm_created", "dtm_updated"]
    opts = instance._meta
    data = {}
    if exclude_none:
        exclude = []

    for f in chain(opts.concrete_fields, opts.many_to_many):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        field_name = f.verbose_name if verbose_name else f.name
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[field_name] = []
            else:
                try:
                    data[field_name] = list(
                        f.value_from_object(instance).values_list("pk", flat=True)
                    )
                except AttributeError:
                    data[field_name] = list(f.value_from_object(instance))
                except FieldDoesNotExist:
                    data[field_name] = []
        else:
            data[field_name] = f.value_from_object(instance)
    return data


class CoreManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class CoreModel(models.Model):
    objects = CoreManager()
    all_objects = models.Manager()

    dtm_created = models.DateTimeField(verbose_name="DTM Created", auto_now_add=True)
    dtm_updated = models.DateTimeField(verbose_name="DTM Updated", auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # slug = prefixed random string
        if hasattr(self, "slug") and not self.slug:
            prefix = getattr(self.__class__, "SLUG_PREFIX", None)
            prefix = prefix + "_" if prefix else ""

            slug_length = self._meta.get_field("slug").max_length - len(prefix)
            self.slug = prefix + self.get_slug(slug_length)
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = prefix + self.get_slug()

        super().save(*args, **kwargs)

    @staticmethod
    def get_slug(slug_length: int = 16):
        return get_random_string(slug_length).lower()

    @classmethod
    def initdata(cls):
        print("{}.initdata()".format(cls.__name__))

    def to_dict(
        self,
        fields=None,
        exclude=None,
        exclude_none=False,
        verbose_name=False,
    ):
        if exclude is None:
            exclude = ["id", "dtm_created", "dtm_updated"]
        return qux_model_to_dict(
            self,
            fields=fields,
            exclude=exclude,
            exclude_none=exclude_none,
            verbose_name=verbose_name,
        )

    @classmethod
    def get_dict(cls, pk):
        result = cls.objects.get(id=pk)
        return result.to_dict()

    def settag(self, tag: str):
        if not hasattr(self, "tags"):
            return

        tags = []
        if self.tags:
            tags = [x.strip() for x in self.tags.split(",")]
        tags.append(tag)
        tags.sort()
        self.tags = ",".join(tags)
        self.save()

    def deltag(self, tag: str):
        if not hasattr(self, "tags"):
            return

        tags = []
        if self.tags:
            tags = [x.strip() for x in self.tags.split(",")]
        if tag in tags:
            tags.remove(tag)
        tags.sort()
        self.tags = ",".join(tags)
        self.save()

    def hastag(self, tag: str):
        if not hasattr(self, "tags"):
            return

        tags = []
        if self.tags and self.tags != "":
            tags = [x.strip() for x in self.tags.split(",")]
        if tag in tags:
            return True
        return False

    def gettags(self):
        if not hasattr(self, "tags"):
            return

        tags = []
        if self.tags and self.tags != "":
            tags = [x.strip() for x in self.tags.split(",")]
        if "" in tags:
            tags.remove("")
        return tags

    @classmethod
    def gettaglist(cls):
        try:
            tags = (
                cls.objects.all()
                .exclude(models.Q(tags__isnull=True) | models.Q(tags=""))
                .values_list("tags", flat=True)
                .distinct()
            )
        except FieldError:
            return

        tags = ",".join(tags)
        tags = [x.strip() for x in tags.split(",")]
        tags = list(set(tags))
        if "" in tags:
            tags.remove("")
        return tags


class CoreModelAdmin(admin.ModelAdmin):
    list_display = (
        "dtm_created",
        "dtm_updated",
    )
    list_filter = (("dtm_created", DateRangeFilter), ("dtm_updated", DateRangeFilter))
    readonly_fields = (
        "dtm_created",
        "dtm_updated",
    )

    list_per_page = 50
    show_full_result_count = False

    # noinspection PyProtectedMember
    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """

        # Default: qs = self.model._default_manager.get_query_set()
        qs = self.model._default_manager.get_queryset()

        # TODO: this should be handled by some parameter to the ChangeList.
        # () because *None is bad
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class CoreManagerPlus(CoreManager):
    def get(self, *args, **kwargs):
        # print("get is_deleted=False")
        return self.get_queryset().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        # print("filter is_deleted=False")
        return self.get_queryset().filter(*args, **kwargs)

    def get_queryset(self):
        # print("get_queryset is_deleted=False")
        return super(CoreManagerPlus, self).get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        # print("all_with_deleted is_deleted=False")
        return super(CoreManagerPlus, self).get_queryset()


class CoreModelPlus(CoreModel):
    objects = CoreManagerPlus()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.dtm_created:
            self.dtm_created = timezone.now()
        self.dtm_updated = timezone.now()
        return super(CoreModelPlus, self).save(*args, **kwargs)

    def delete(self, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class CoreModelPlusAdmin(admin.ModelAdmin):
    list_display = (
        "is_deleted",
        "dtm_created",
        "dtm_updated",
    )
    list_filter = (
        "is_deleted",
        ("dtm_created", DateRangeFilter),
        ("dtm_updated", DateRangeFilter),
    )
    readonly_fields = (
        "dtm_created",
        "dtm_updated",
    )

    list_per_page = 50
    show_full_result_count = False

    # noinspection PyProtectedMember
    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """

        # Default: qs = self.model._default_manager.get_query_set()
        qs = self.model._default_manager.all_with_deleted()

        # TODO: this should be handled by some parameter to the ChangeList.
        # () because *None is bad
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
