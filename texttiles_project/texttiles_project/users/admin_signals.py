import logging
from django.contrib.admin.models import LogEntry
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger("admin")

ACTION_MAP = {1: "ADD", 2: "CHANGE", 3: "DELETE"}


@receiver(post_save, sender=LogEntry)
def admin_actions(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f"ADMIN ACTION | User: {instance.user.username} | "
            f"Action: {ACTION_MAP.get(instance.action_flag)} | "
            f"Model: {instance.content_type.model} | "
            f"Object: {instance.object_repr}"
        )
