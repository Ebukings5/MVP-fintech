from django.urls import path, include
from .views import UserCreateView, CategoryViewSet, ExpenseViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('', include(router.urls)),
]