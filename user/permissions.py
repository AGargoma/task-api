from rest_framework import permissions


class IsOwnerOrAdmin(permissions.IsAdminUser):
    message = 'Resource can be accessed only by owner'

    def has_object_permission(self, request, view, obj):
        print(obj.user)
        return super(self).has_object_permission(request,view,obj) or obj.user == request.user
