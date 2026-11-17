import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrganizationsConfig(AppConfig):
    """OrganizationsConfig class.

    The organizations app is for managing organizations. It provides models for organizations,
    organization types, and organization types.

    """

    name = "lideresas.apps.organizations"
    verbose_name = _("Organizations")

    def ready(self):
        with contextlib.suppress(ImportError):
            import lideresas.apps.organizations.signals  # noqa: F401
