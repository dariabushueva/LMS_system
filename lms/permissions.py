from rest_framework.permissions import BasePermission


class IsModeratorOrIsAuthor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return request.user == view.get_object().author


class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().author or request.user.is_superuser:
            return True


class IsSubscriber(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().subscriber or request.user.is_superuser:
            return True

