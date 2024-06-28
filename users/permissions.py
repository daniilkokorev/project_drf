from rest_framework import permissions


class Moderator(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
         return request.user.groups.filter(name='moders').exists()
