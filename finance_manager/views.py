from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import (
    UserSerializer,
    RegisterSerializer,
    CategorySerializer,
    ExpenseSerializer,
    TransactionSerializer,
    BudgetSerializer,
)
from .models import Expense, Category, Budget, Transaction, CustomUser
from django.db.models import Sum
import csv
from rest_framework.views import exception_handler, APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
#from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_expense = Expense.objects.filter(user=request.user).aggregate(total_expense=Sum('amount'))['total_expense'] or 0
        return Response({"total_expense": total_expense})

class ExportDataView(APIView):
    permission_classes = [IsAuthenticated]

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
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data
            return Response({
                'refresh': str(tokens['refresh']),
                'access': str(tokens['access']),
            })
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

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
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, serializers.ValidationError):
            response.data = {
                'error': 'Invalid data',
                'details': response.data
            }
        elif isinstance(exc, NotFound):
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, PermissionDenied):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

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
