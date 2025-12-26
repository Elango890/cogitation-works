import logging
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

logger = logging.getLogger("auth")


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    logger.info(
        f"LOGIN | User: {user.username} | Email: {user.email} | Role: {'Admin' if user.is_staff else 'User'}"
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    logger.info(
        f"LOGOUT | User: {user.username} | Email: {user.email}"
    )
