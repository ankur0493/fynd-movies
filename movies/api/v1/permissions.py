from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import exceptions, permissions


class MoviePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff
