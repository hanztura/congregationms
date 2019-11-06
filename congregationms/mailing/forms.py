from django.forms import FilePathField, ModelForm
from django.core.mail import get_connection, send_mail, EmailMessage

from .models import Mail, UserMail


class UserMailModelForm(ModelForm):

    class Meta:
        model = UserMail
        fields = [
            'server',
            'tls',
            'tls_port',
            'name',
            'email_address',
            'password',
        ]


class MailModelForm(ModelForm):

    class Meta:
        model = Mail
        fields = [
            'to',
            'subject',
            'message',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.fields['filename'].required = True
        super().__init__(*args, **kwargs)

    def save(self, commit=False):
        mail = super().save(commit=commit)
        mail.user_mail = self.user.mail
        mail.save()

        return mail

    def send_email(self, attachment):
        user_mail = self.instance.user_mail

        # connection settings
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

        # mail content
        mail = self.instance
        subject = mail.subject
        message = mail.message
        recipient_list = [mail.to, ]

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=username,
            to=recipient_list,
            connection=connection
        )
        email.attach_file(attachment)
        mail_result = email.send(fail_silently=False)

        if mail_result:
            self.instance.sent = True
            self.instance.save()

        return mail_result
