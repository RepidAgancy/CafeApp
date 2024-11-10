import django_filters
from django.db.models import Q

from product import models


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search')
    class Meta:
        model = models.Product
        fields = ['search']

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(name_uz__icontains=value)|
            Q(name_ru__icontains=value)|
            Q(name_en__icontains=value)
        )


