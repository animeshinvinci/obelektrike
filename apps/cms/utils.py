from django.core.mail import send_mail as django_send_mail

from apps.cms.models import CmsEmail


def send_mail(subject, message, from_email, recipient_list, **kwargs):
    django_send_mail(subject, message, from_email, recipient_list, **kwargs)
    email = CmsEmail(
        from_email=from_email,
        to_emails=', '.join(recipient_list),
        subject=subject,
        body=message,
    )
    email.save()
