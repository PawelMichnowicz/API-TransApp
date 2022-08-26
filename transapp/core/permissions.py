from rest_framework.permissions import BasePermission
from rest_framework import serializers
from core.constants import WorkPosition
from storage.models import Warehouse
from django.shortcuts import get_object_or_404

class IsDirector(BasePermission):
    ''' Check if request user position is Director'''
    def has_permission(self, request, view):
        return request.user.position == WorkPosition.DIRECTOR.value or request.user.position == WorkPosition.ADMIN.value


class IsAdmin(BasePermission):
    ''' Check if request user position is Admin'''
    def has_permission(self, request, view):
        return request.user.position == WorkPosition.ADMIN.value or request.user.position == WorkPosition.ADMIN.value


class IsCoordinator(BasePermission):
    ''' Check if request user position is Coordinator'''
    def has_permission(self, request, view):
        return request.user.position == WorkPosition.COORDINATOR.value or request.user.position == WorkPosition.ADMIN.value


class WorkHere(BasePermission):
    ''' Check if request user work in consider warehouse'''
    def has_object_permission(self, request, view, obj):
        return request.user.workplace == obj or request.user.workplace == obj.warehouse or request.user.position == WorkPosition.ADMIN.value

class WorkHereActionObject(BasePermission):
    ''' Check if request user work in consider warehouse received from Action object'''
    def has_object_permission(self, request, view, obj):
        return request.user.workplace == obj.warehouse or request.user.position == WorkPosition.ADMIN.value

class WorkHereActionWindow(BasePermission):

    def has_permission(self, request, view):
        pk_warehouse = int(request.data['warehouse'])
        warehouse = get_object_or_404(Warehouse, pk=pk_warehouse)
        return request.user.workplace == warehouse or request.user.position == WorkPosition.ADMIN.value
