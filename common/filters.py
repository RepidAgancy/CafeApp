import django_filters
from django.db.models import Q

from common import models


class FoodFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    class Meta:
        model = models.Food
        fields = ['search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name_uz__icontains=value) |
            Q(name_ru__icontains=value) |
            Q(name_en__icontains=value)
        )
