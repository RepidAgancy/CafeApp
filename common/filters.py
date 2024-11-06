import django_filters

from common import models


class FoodFilter(django_filters.FilterSet):
    class Meta:
        model = models.Food
        fields = {'name': ['icontains']}

