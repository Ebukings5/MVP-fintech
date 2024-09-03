# core/tests.py

from django.test import TestCase
from .models import UserProfile, Transaction, Budget
from django.contrib.auth.models import User

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