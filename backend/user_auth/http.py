from http import HTTPStatus

from django.http import HttpResponse


class HttpResponseUnauthorized(HttpResponse):
    status_code = HTTPStatus.UNAUTHORIZED


class HttpResponseConflict(HttpResponse):
    status_code = HTTPStatus.CONFLICT