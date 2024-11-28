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
            Q(name__icontains=value)
        )


class OrderListInProcessFilter(django_filters.FilterSet):
    table_number = django_filters.NumberFilter(method='filter_table')

    class Meta:
        model = models.Order
        fields = ['table_number']

    def filter_table(self, queryset, name, value):
        return queryset.filter(
            cart__table__number__icontains=value
        )