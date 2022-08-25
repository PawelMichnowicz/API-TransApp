from rest_framework.permissions import BasePermission
from rest_framework import serializers
from core.models import WorkPosition
from storage.models import Warehouse


class IsDirector(BasePermission):

    def has_permission(self, request, view):

        return request.user.position == WorkPosition.DIRECTOR.value or request.user.position == WorkPosition.ADMIN.value


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.position == WorkPosition.ADMIN.value or request.user.position == WorkPosition.ADMIN.value


class IsCoordinator(BasePermission):

    def has_permission(self, request, view):
        return request.user.position == WorkPosition.COORDINATOR.value or request.user.position == WorkPosition.ADMIN.value


class WorkHere(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.workplace == obj or request.user.workplace == obj.warehouse or request.user.position == WorkPosition.ADMIN.value

class WorkHereActionObject(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.workplace == obj.warehouse or request.user.position == WorkPosition.ADMIN.value

class WorkHereActionWindow(BasePermission):

    def has_permission(self, request, view):
        pk_warehouse = int(request.data['warehouse'])
        warehouse = Warehouse.objects.get(pk=pk_warehouse)
        return request.user.workplace == warehouse or request.user.position == WorkPosition.ADMIN.value
