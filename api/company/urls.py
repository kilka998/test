from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, DepartmentViewSet


router = DefaultRouter(trailing_slash=True)

router.register('employees', EmployeeViewSet, basename='employees')
router.register('departments', DepartmentViewSet, basename='departments')


urlpatterns = [
   path('', include(router.urls)),
]
