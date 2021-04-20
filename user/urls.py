from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()
# router.register(r'permission', views.PermissionViewSet)
router.register(r'users', views.UserViewSet,basename='user')
router.register(r'registraion',views.RegistrationViewSet,basename='registration')
urlpatterns = [
    path('', include(router.urls)),
]