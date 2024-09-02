from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Expense, Transaction, Budget
from django.contrib.auth.password_validation import validate_password
import datetime
from django.db.models import Sum

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'user']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'date', 'description', 'user']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        if data['date'] > datetime.date.today():
            raise serializers.ValidationError("Transaction date cannot be in the future.")
        return data

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        user_profile = validated_data['user'].profile

        if transaction.type == 'income':
            user_profile.balance += transaction.amount
        elif transaction.type == 'expense':
            if user_profile.balance >= transaction.amount:
                user_profile.balance -= transaction.amount
            else:
                raise ValidationError("Insufficient balance for this transaction.")

        user_profile.save()
        return transaction

    def update(self, instance, validated_data):
        user_profile = instance.user.profile

        # Reverse the effect of the previous transaction
        if instance.type == 'income':
            user_profile.balance -= instance.amount
        elif instance.type == 'expense':
            user_profile.balance += instance.amount

        # Apply the new transaction details
        instance.amount = validated_data.get('amount', instance.amount)
        instance.type = validated_data.get('type', instance.type)

        if instance.type == 'income':
            user_profile.balance += instance.amount
        elif instance.type == 'expense':
            if user_profile.balance >= instance.amount:
                user_profile.balance -= instance.amount
            else:
                raise ValidationError("Insufficient balance for this transaction.")

        user_profile.save()
        instance.save()
        return instance

    def validate(self, data):
        user_profile = data['user'].profile
        transaction_type = data['type']
        transaction_amount = data['amount']

        if transaction_type == 'expense':
            category = data['category']
            total_spent = Transaction.objects.filter(user=user_profile.user, type='expense', category=category).aggregate(total=Sum('amount'))['total'] or 0
            budget = Budget.objects.get(user=user_profile.user, category=category)

            if total_spent + transaction_amount > budget.amount:
                raise ValidationError("This transaction exceeds your budget for this category.")

        return data

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data