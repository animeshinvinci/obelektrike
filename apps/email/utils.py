from django.core.mail import send_mail as django_send_mail

from apps.email.models import Email


def send_mail(subject, message, from_email, recipient_list, **kwargs):
    django_send_mail(subject, message, from_email, recipient_list, **kwargs)
    Email(
        from_email=from_email,
        to_emails=', '.join(recipient_list),
        subject=subject,
        body=message,
    )
    # email.save()
