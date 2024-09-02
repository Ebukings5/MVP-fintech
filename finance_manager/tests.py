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
