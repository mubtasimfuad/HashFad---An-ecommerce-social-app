from rest_framework import permissions



class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        else:
            return True
       