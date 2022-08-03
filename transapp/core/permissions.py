from rest_framework.permissions import BasePermission
from core.models import WorkPosition

class IsDirector(BasePermission):

    def has_permission(self, request, view):
        return request.user.position == WorkPosition.DIRECTOR.value


class WorkHere(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.workplace == obj