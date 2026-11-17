import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """UsersConfig class.
    The users app is for managing users. It provides models for users,
    user roles, and user permissions.

    """

    name = "lideresas.apps.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import lideresas.apps.users.signals  # noqa: F401
