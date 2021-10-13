from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import send_code

router = DefaultRouter()

urlpatterns = [
    path('v1/auth/signup', send_code, name='send_code')
]