from rest_framework.permissions import BasePermission
from core.models import WorkPosition

class IsDirector(BasePermission):

    def has_permission(self, request, view):
        return request.user.position == WorkPosition.DIRECTOR.value or request.user.position == WorkPosition.ADMIN.value


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.position == WorkPosition.ADMIN.value


class WorkHere(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.workplace == obj