from django.core.mail import EmailMessage
from django.conf import settings


def send_report_email(user, file_buffer, filename):
    email = EmailMessage(
        subject="Outstanding Report",
        body="Please find attached the Outstanding Report.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach(
        filename,
        file_buffer.read(),
        "application/octet-stream"
    )

    email.send()
