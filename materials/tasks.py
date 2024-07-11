from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Subscriptions


@shared_task
def course_update_message(course_id):
    """Сообщение об обновлении курса"""
    mailing = Subscriptions.objects.filter(course=course_id, status=True)
    for mail in mailing:
        course = mail.course
        user = mail.owner
        send_mail(
            subject=f'{course} обновился',
            message=f'{course} обновился',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        print(f'Сообщение отправлено {user.email}')
