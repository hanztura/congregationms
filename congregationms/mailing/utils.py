from django.core.mail import get_connection
from django.core.mail import send_mail

from .models import UserMail


def send_email(user_mail):
    # user_mail = self.instance.user_mail
    host = user_mail.server
    username = user_mail.email_address
    password = user_mail.password
    use_tls = user_mail.tls
    port = user_mail.tls_port
    connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        fail_silently=False,
        host=host,
        port=port,
        username=username,
        password=password,
        use_tls=use_tls
    )
    mail_result = send_mail('test', 'hello world', username,
                            ['hanz@xofytech.com', ], connection=connection)
    return mail_result


def user_has_no_mail(pk):
    mail = UserMail.objects.filter(user=pk)
    if mail.count() < 1:
        return True
    else:
        return False
