from django.conf import settings
from django.core.mail import EmailMessage

import threading


class SendMail(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.args = args
        self.kwargs = kwargs

    def proceed(self):
        self.start()

    def run(self):
        if self.kwargs.get("verify_email"):
            self.send_email_verification_code(*self.args)
        if self.kwargs.get("password_reset"):
            self.send_password_reset_link(*self.args)

    def send_password_reset_link(self, content, recipient):
        mail = EmailMessage(
            subject="[Celesup] Password Reset Link",
            body=content,
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient],
        )
        return self.send(mail)

    def send_email_verification_code(self, content, recipient):
        """sends verifications email to the recipient list\n* This can take some minutes"""
        mail = EmailMessage(
            subject="[Celesup] Confirm Email Address",
            body=content,
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient],
        )
        return self.send(mail)

    def send(self, mail: EmailMessage):
        sended = False
        mail.content_subtype = "html"
        try:
            sended = mail.send(fail_silently=False)
        except Exception as e:
            print(e)

        if sended:
            return True
        return False
