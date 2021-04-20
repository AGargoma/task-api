from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from task import views
from task.views import download

router = DefaultRouter()
router.register(r'task', views.TaskViewSet)
router.register(r'tasks',views.TaskManagerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]