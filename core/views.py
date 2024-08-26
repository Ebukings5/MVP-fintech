from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer
from .models import Expense, Category
from .serializer import CategorySerializer, ExpenseSerializer
from django.db.models import Sum
import csv
from django.http import HttpResponse

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
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
# Compare this snippet from alx/MVP-fintech/finance_manager/core/urls.py: