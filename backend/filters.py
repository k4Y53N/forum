from math import ceil

from django.db.models import QuerySet
from django.forms import Form
from forum.models import Topic

class Filter:
    queryset = QuerySet()
    query_expr = {}
    form_class = Form
    page_size = None

    def __init__(self, request, query_data: dict, queryset=None, query_kwargs=None, form_class=None) -> None:
        self.request = request
        self.query_data = query_data
        if queryset != None:
            self.queryset=queryset
        if query_kwargs != None:
            self.query_expr = query_kwargs
        if form_class != None:
            self.form_class = form_class

    def __iter__(self):
        for index, obj in enumerate(self.get_queryset()):
            yield self.perform(obj, index)

    @property
    def data(self):
        if not bool(self.page_size):
            return [perform_data for perform_data in self]

        page = self.query_data.get('page', 1)
    
        if type(page) != int:
            page = 1
            
        if page <= 0:
            page = 1

        queryset = self.get_queryset()
        count = queryset.count()
        page_count = ceil(count / self.page_size) if count != 0 else 0
        if page > page_count:
            page = page_count

        head = self.page_size * (page - 1)
        limit = head + self.page_size
        queryset = queryset[head:limit]

        return {
            'page': page,
            'page_count': page_count,
            'data': [
                self.perform(obj, index + head)
                for index, obj in enumerate(queryset)
            ]
        }

    def get_queryset(self):
        queryset = self.queryset
        query_kwargs = self.get_query_kwargs()

        return queryset.filter(**query_kwargs)

    def get_query_kwargs(self):
        form = self.form_class(self.query_data)
        query_data = {}
        if form.is_valid():
            query_data = form.cleaned_data
        query_kwargs = {}
        for key, expr in self.query_expr.items():
            query_value = query_data.get(key)
            if query_value != None:
                query_kwargs[expr] = query_value

        return query_kwargs

    def perform(self, obj, index):
        pass
