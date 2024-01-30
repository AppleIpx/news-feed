from django_filters.rest_framework import FilterSet, filters
from news.models import BlogPost


class NewsFilter(FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFilter(
        field_name='created_at',
        lookup_expr='date'
    )

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'created_at',
        ]
