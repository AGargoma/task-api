from django.contrib.auth.models import Permission
from django.shortcuts import render
from rest_framework import viewsets, permissions,mixins

from user.models import User
from user.serializers import UserSerializer#, PermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# class PermissionViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows permissions to be viewed or edited.
#     """
#     queryset = Permission.objects.all()
#     serializer_class = PermissionSerializer

class RegistrationViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
