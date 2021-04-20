from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quiz import views

router = DefaultRouter()
router.register(r'quizz', views.QuizViewSet)
router.register(r'quizzes', views.QuizManagerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]