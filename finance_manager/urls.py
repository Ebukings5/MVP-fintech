from django.urls import path, include
from .views import UserCreateView, CategoryViewSet, ExpenseViewSet
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionListCreateView,
    TransactionDetailView,
    BudgetListCreateView,
    BudgetDetailView,
    UserDetailView,
    SpendingSummaryView,
    RegisterView
)
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', include('rest_framework.urls')),  # Include DRF URLs
    path('spending-summary/', SpendingSummaryView.as_view(), name='spending-summary'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     # Transaction Management
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:id>/', TransactionDetailView.as_view(), name='transaction-detail'),

    # Budget Management
    path('budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budgets/<int:id>/', BudgetDetailView.as_view(), name='budget-detail'),

    # User Management
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('', include(router.urls)),
]