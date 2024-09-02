from celery import shared_task
from django.core.mail import send_mail
from .models import Notification, UserProfile
from datetime import datetime, timedelta


@shared_task
def send_notification(user_id, message):
    user = User.objects.get(id=user_id)
    send_mail(
        'Notification',
        message,
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
@shared_task
def send_upcoming_bill_notifications():
    users = UserProfile.objects.all()
    for user in users:
        notifications = Notification.objects.filter(user=user, date__lte=datetime.now() + timedelta(days=3), sent=False)
        for notification in notifications:
            send_mail(
                'Upcoming Bill Reminder',
                f'Dear {user.user.first_name}, you have an upcoming bill: {notification.description} due on {notification.date}.',
                'from@example.com',
                [user.user.email],
                fail_silently=False,
            )
            notification.sent = True
            notification.save()

@shared_task
def send_budget_limit_alerts():
    users = UserProfile.objects.all()
    for user in users:
        budgets = Budget.objects.filter(user=user)
        for budget in budgets:
            total_spent = Transaction.objects.filter(user=user, type='expense', category=budget.category).aggregate(total=Sum('amount'))['total'] or 0
            if total_spent > budget.amount * 0.9 and not budget.alert_sent:
                send_mail(
                    'Budget Limit Alert',
                    f'Dear {user.user.first_name}, you are close to reaching your budget limit for {budget.category.name}.',
                    'from@example.com',
                    [user.user.email],
                    fail_silently=False,
                )
                budget.alert_sent = True
                budget.save()