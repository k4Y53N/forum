from math import ceil

from django.db.models import QuerySet


class Filter:
    queryset: QuerySet = QuerySet.none()
    lookup_fields = {}
    page_size = None

    def __init__(self, request, clean_data: dict) -> None:
        self.request = request
        self.clean_data = clean_data

    def __iter__(self):
        for index, obj in enumerate(self.get_queryset()):
            yield self.perform(obj, index)

    @property
    def data(self):
        if not bool(self.page_size):
            return [perform_data for perform_data in self]

        page = self.clean_data.get('page', 1)
        if type(page) != int:
            raise TypeError('page must be interger')
        if page < 0:
            page = 1

        queryset = self.get_queryset()
        count = queryset.count()
        page_count = ceil(count / self.page_size) if count != 0 else 0
        if page > page_count:
            page = page_count

        head = self.page_size * page
        limit = head + self.page_size
        queryset = queryset[head:limit]

        return {
            'page': page,
            'page_count': page_count,
            'data': [
                self.perform(obj, index)
                for index, obj in enumerate(queryset)
            ]
        }

    def get_queryset(self):
        queryset = self.queryset
        query_kwargs = self.get_query_kwargs()

        return queryset.filter(**query_kwargs)

    def get_query_kwargs(self):
        query_kwargs = {}
        for key, query_field in self.get_query_kwargs():
            query_value = self.clean_data.get(key)
            if query_value != None:
                query_kwargs[query_field] = query_value

        return query_kwargs

    def perform(self, obj, index):
        pass
