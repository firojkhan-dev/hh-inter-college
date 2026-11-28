import logging
import smtplib

from django.conf import settings
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


def notify_college_staff(subject, message):
    recipient = settings.COLLEGE_NOTIFICATION_EMAIL
    if not recipient:
        logger.warning(
            "College email notification was not sent: "
            "COLLEGE_NOTIFICATION_EMAIL is not configured."
        )
        return False

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except (OSError, smtplib.SMTPException):
        logger.exception("Could not send a college notification email.")
        return False
    return True
