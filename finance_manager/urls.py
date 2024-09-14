from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserCreateView,
    RegisterView,
    CustomTokenObtainPairView,
    TransactionListCreateView,
    TransactionDetailView,
    BudgetListCreateView,
    BudgetDetailView,
    UserDetailView,
    SpendingSummaryView,
    CategoryViewSet,
    ExpenseViewSet,
    ReportView,
    ExportDataView
)
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the home page!")

# Setting up the router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', home, name='home'),  # This handles the root URL
    path('api/', include(router.urls)),
    path('api/', include('rest_framework.urls')),  # Include DRF URLs

    # User Management
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/register/complete/', RegisterView.as_view(), name='register_complete'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Transaction Management
    path('api/transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('api/transactions/<int:id>/', TransactionDetailView.as_view(), name='transaction-detail'),

    # Budget Management
    path('api/budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('api/budgets/<int:id>/', BudgetDetailView.as_view(), name='budget-detail'),

    # User Detail Management
    path('api/users/<int:id>/', UserDetailView.as_view(), name='user-detail'),

    # Spending Summary
    path('api/spending-summary/', SpendingSummaryView.as_view(), name='spending-summary'),

    # Additional Views
    path('api/report/', ReportView.as_view(), name='report'),
    path('api/export/', ExportDataView.as_view(), name='export_data'),
]
