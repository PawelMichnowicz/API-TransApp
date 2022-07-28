from rest_framework.permissions import BasePermission
from core.constants import WORK_POSITION

class IsDirector(BasePermission):

    def has_permission(self, request, view):
        return request.user.position == WORK_POSITION[2]


class WorkHere(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.workplace == obj