from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(post_save, sender=get_user_model())
def user_signal(sender, created, instance, **kwargs):
    """[TODO:summary]

    Args:
        sender ([TODO:type]): [TODO:description]
        created ([TODO:type]): [TODO:description]
        instance ([TODO:type]): [TODO:description]
    """
    if created and instance.username is None:
        instance.username = "U%(id)s" % {"id": 1000 + instance.id}
        instance.save()
