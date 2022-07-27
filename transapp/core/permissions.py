from rest_framework.permissions import BasePermission

class IsDirector(BasePermission):

    def has_permission(self, request, view):
        return request.user.position == 'DIR'


class WorkHere(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.workplace == obj