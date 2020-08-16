from rest_framework import permissions

class IsSuper(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            user = request.user
            return True/False