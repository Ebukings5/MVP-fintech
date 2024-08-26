from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = { 'password': {'write_only': True, 'required': True} }
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