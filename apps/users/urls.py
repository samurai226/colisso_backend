"""
Users URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet, AffectationGareViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'users', UserViewSet, basename='user')
router.register(r'affectations', AffectationGareViewSet, basename='affectation')

urlpatterns = [
    path('', include(router.urls)),
]
