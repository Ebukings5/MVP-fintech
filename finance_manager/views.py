from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import UserSerializer, RegisterSerializer, CategorySerializer, ExpenseSerializer, TransactionSerializer, BudgetSerializer
from .models import Expense, Category, Budget, Transaction, CustomUser  # Ensure CustomUser is imported
from django.db.models import Sum
import csv
from rest_framework.views import exception_handler, APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()  # Use CustomUser
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ReportView(APIView):
    def get(self, request, *args, **kwargs):
        total_expense = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))
        return Response({"total_expense": total_expense})

class ExportDataView(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

        writer = csv.writer(response)
        writer.writerow(['Category', 'Amount', 'Date', 'Description'])

        expenses = Expense.objects.filter(user=request.user)
        for expense in expenses:
            writer.writerow([expense.category.name, expense.amount, expense.date, expense.description])

        return response

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()  # Use CustomUser
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user_profile = instance.user.profile
        if instance.type == 'income':
            user_profile.balance -= instance.amount
        elif instance.type == 'expense':
            user_profile.balance += instance.amount
        user_profile.save()
        instance.delete()

class BudgetListCreateView(generics.ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()  # Use CustomUser
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def custom_exception_handler(exc, context):
        response = exception_handler(exc, context)

        if isinstance(exc, serializers.ValidationError):
            response.data = {
                'error': 'Invalid data',
                'details': response.data
        }

        elif isinstance(exc, NotFound):
            response = Response({
                'error': 'Not found'
        }, status=status.HTTP_404_NOT_FOUND)

        elif isinstance(exc, PermissionDenied):
            response = Response({
            'error': 'Permission denied'
        }, status=status.HTTP_403_FORBIDDEN)

        return response

class SpendingSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_income = Transaction.objects.filter(user=user, type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Transaction.objects.filter(user=user, type='expense').aggregate(total=Sum('amount'))['total'] or 0
        savings = total_income - total_expense

        category_spending = Transaction.objects.filter(user=user, type='expense').values('category__name').annotate(total=Sum('amount'))

        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'savings': savings,
            'category_spending': category_spending
        })