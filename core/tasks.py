from celery import shared_task
from django.core.mail import send_mail

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