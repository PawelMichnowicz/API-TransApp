from rest_framework.permissions import BasePermission

class IsDirector(BasePermission):

    def has_permission(self, request, view):
        return request.user.position == 'DIR'