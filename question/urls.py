from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from question import views

router = SimpleRouter()
router.register(r'question', views.QuestionViewSet)
router.register(r'choice',views.ChoiceViewSet)
router.register(r'questions', views.QuestionManagerViewSet)
router.register(r'choices',views.ChoiceManagerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]