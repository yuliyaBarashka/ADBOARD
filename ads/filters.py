import django_filters
from .models import Ad


class AdFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    type = django_filters.ChoiceFilter(choices=Ad.TYPE_CHOICES)   # ← НОВОЕ

    class Meta:
        model = Ad
        fields = ['title', 'min_price', 'max_price', 'type']
