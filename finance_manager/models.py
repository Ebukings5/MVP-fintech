from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')  # Ensure category names are unique per user
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        # Custom validation logic for Category
        if not self.name:
            raise ValidationError('Category name cannot be empty')

class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']  # Order expenses by date descending

    def __str__(self):
        return f'{self.amount} - {self.category.name} on {self.date}'

    def clean(self):
        # Custom validation logic for Expense
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than zero')

class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f'Budget for {self.category.name}: {self.amount} from {self.start_date} to {self.end_date}'

    def clean(self):
        # Custom validation logic for Budget
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date')
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than zero')

    def is_exceeded(self):
        total_expenses = Expense.objects.filter(
            category=self.category,
            date__range=[self.start_date, self.end_date]
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        return total_expenses > self.amount

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.type}: {self.amount} on {self.date} for {self.category.name}'

    def clean(self):
        # Custom validation logic for Transaction
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than zero')
        if self.type not in dict(self.TYPE_CHOICES).keys():
            raise ValidationError('Invalid transaction type')
