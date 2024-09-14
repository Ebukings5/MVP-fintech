from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import Notification, UserProfile, Budget, Transaction
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification(user_id, message):
    user = get_object_or_404(User, id=user_id)
    try:
        send_mail(
            'Notification',
            message,
            'your_email@example.com',  # Use an environment variable for email sender
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send notification to {user.email}: {e}")

@shared_task
def send_upcoming_bill_notifications():
    users = UserProfile.objects.prefetch_related('user').all()
    for user in users:
        notifications = Notification.objects.filter(
            user=user,
            date__lte=datetime.now() + timedelta(days=3),
            sent=False
        )
        for notification in notifications:
            try:
                send_mail(
                    'Upcoming Bill Reminder',
                    f'Dear {user.user.first_name}, you have an upcoming bill: {notification.description} due on {notification.date}.',
                    'your_email@example.com',  # Use an environment variable for email sender
                    [user.user.email],
                    fail_silently=False,
                )
                notification.sent = True
                notification.save()
            except Exception as e:
                logger.error(f"Failed to send notification for bill to {user.user.email}: {e}")

@shared_task
def send_budget_limit_alerts():
    users = UserProfile.objects.prefetch_related('user').all()
    budgets_to_update = []
    for user in users:
        budgets = Budget.objects.filter(user=user)
        for budget in budgets:
            total_spent = Transaction.objects.filter(
                user=user.user,
                type='expense',
                category=budget.category,
                date__range=[budget.start_date, datetime.now()]  # Consider transactions within budget period
            ).aggregate(total=Sum('amount'))['total'] or 0

            if total_spent > budget.amount * 0.9 and not budget.alert_sent:
                try:
                    send_mail(
                        'Budget Limit Alert',
                        f'Dear {user.user.first_name}, you are close to reaching your budget limit for {budget.category.name}. You have spent {total_spent} out of your {budget.amount} budget.',
                        'your_email@example.com',  # Use an environment variable for email sender
                        [user.user.email],
                        fail_silently=False,
                    )
                    budget.alert_sent = True
                    budgets_to_update.append(budget)
                except Exception as e:
                    logger.error(f"Failed to send budget alert to {user.user.email}: {e}")

    # Bulk update budgets to reduce the number of database hits
    Budget.objects.bulk_update(budgets_to_update, ['alert_sent'])

@shared_task
def reset_budget_alerts():
    # Reset the `alert_sent` field for budgets at the start of each new period (e.g., monthly)
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    budgets = Budget.objects.filter(end_date__gte=start_of_month, alert_sent=True)
    for budget in budgets:
        budget.alert_sent = False

    # Bulk update budgets to reduce the number of database hits
    Budget.objects.bulk_update(budgets, ['alert_sent'])