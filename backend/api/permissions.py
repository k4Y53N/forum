from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user