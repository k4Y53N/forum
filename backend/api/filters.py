from django_filters.filters import CharFilter
from django_filters import FilterSet
from forum.models import Topic


class TopicFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')