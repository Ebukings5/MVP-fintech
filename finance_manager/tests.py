from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import UserProfile, Transaction, Budget, Category, Expense
from .serializers import UserSerializer, TransactionSerializer, BudgetSerializer, CategorySerializer, ExpenseSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user, balance=1000)

    def test_profile_creation(self):
        self.assertEqual(self.profile.balance, 1000)

    def test_balance_update(self):
        self.profile.balance += 500
        self.profile.save()
        self.assertEqual(self.profile.balance, 1500)

    def test_negative_balance(self):
        self.profile.balance = -100
        with self.assertRaises(ValueError):
            self.profile.save()

class TransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user, balance=1000)

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            user=self.user,
            type='expense',
            amount=200,
            description='Groceries'
        )
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.type, 'expense')

    def test_transaction_negative_amount(self):
        with self.assertRaises(ValueError):
            Transaction.objects.create(
                user=self.user,
                type='expense',
                amount=-100,
                description='Invalid Transaction'
            )

    def test_multiple_transactions(self):
        Transaction.objects.create(user=self.user, type='expense', amount=100, description='Rent')
        Transaction.objects.create(user=self.user, type='income', amount=500, description='Salary')
        
        transactions = Transaction.objects.filter(user=self.user)
        self.assertEqual(transactions.count(), 2)

class BudgetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user, balance=1000)
        self.budget = Budget.objects.create(user=self.profile, category='Food', amount=300)

    def test_budget_creation(self):
        self.assertEqual(self.budget.category, 'Food')
        self.assertEqual(self.budget.amount, 300)

    def test_budget_update(self):
        self.budget.amount += 200
        self.budget.save()
        self.assertEqual(self.budget.amount, 500)

    def test_budget_exceedance(self):
        # Assuming you have a method to check if the budget is exceeded
        Transaction.objects.create(user=self.user, type='expense', amount=350, description='Dining Out')
        self.assertTrue(self.budget.is_exceeded())  # Example method, implement accordingly

class APIEndpointsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

    def test_register_user(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = reverse('token_obtain_pair')
        data = {'email': 'testuser@example.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_transaction_list_create(self):
        url = reverse('transaction-list-create')
        data = {'type': 'expense', 'amount': 100, 'description': 'Test Expense'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().description, 'Test Expense')

    def test_budget_list_create(self):
        url = reverse('budget-list-create')
        data = {'category': 'Entertainment', 'amount': 500}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(Budget.objects.get().category, 'Entertainment')

    def test_user_detail(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_spending_summary(self):
        url = reverse('spending-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expense', response.data)
        self.assertIn('savings', response.data)

    def test_export_data(self):
        url = reverse('export_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_report(self):
        url = reverse('report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_expense', response.data)
