"""learneng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from question.urls import router as question_router
from task.views import download
from user.urls import router as user_router
from quiz.urls import router as quiz_router
from task.urls import router as task_router


router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(question_router.registry)
router.registry.extend(quiz_router.registry)
router.registry.extend(task_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^download/(?P<user>[\w]+)/(?P<filename>[\w]+)\.(?P<ext>[\w]+)$', download),

]
