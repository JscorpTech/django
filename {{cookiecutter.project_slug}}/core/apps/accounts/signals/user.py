from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def user_signal(sender, created, instance, **kwargs):
    """Assign a stable default username without triggering recursive saves."""
    if created and instance.username is None:
        sender.objects.filter(pk=instance.pk, username__isnull=True).update(
            username="U%(id)s" % {"id": 1000 + instance.id}
        )
