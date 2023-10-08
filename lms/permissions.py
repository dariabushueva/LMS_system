from rest_framework.permissions import BasePermission


class IsModeratorOrIsAuthor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().author


class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object().author


class IsSubscriber(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object().subscriber

