from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def thanks_for_sing_up(
        user_first_name,
        user_email
):
    subject = 'Thank you for signing up'
    message = f'Уважаемый {user_first_name},\n\n' \
              f'Добро пожаловать на наш портал! Мы рады видеть вас здесь.\n' \
              f'Вы успешно зарегистрировались, и теперь у вас есть доступ к нашим сервисам.\n' \
              f'Если у вас возникнут вопросы или вам потребуется помощь, не стесняйтесь обращаться к нам.\n\n' \
              f'С уважением,\n' \
              f'Команда портала'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
