from django.db.models.signals import post_save
from django.dispatch import receiver

from lideresas.apps.users.models import User

from .models import Dashboard


@receiver(post_save, sender=User)
def on_new_user_create_dashboard(sender, instance, created, **kwargs):
    """Create dashboard signal.

    Description: This signal is used to create a dashboard for a user.
        It is used to create a dashboard for a user.
        It is only called when a new user is created.
        It is only called when the user is a staff user.
        It creates a dashboard for the user if it does not exist.
    Args:
        sender (Any): The sender of the signal.
        instance (User): The instance of the signal.
        created (bool): Whether the instance was created.
        **kwargs: Additional keyword arguments.
    """
    if not created:
        return

    user: User = instance
    if not user.is_staff:
        return

    dashboard, created = Dashboard.objects.get_or_create(admin=user)
    dashboard.save()
