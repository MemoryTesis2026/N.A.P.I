import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardConfig(AppConfig):
    """DashboardConfig class.

    The dashboard app is for managing the dashboard.
    It provides models for the dashboard.
    It also provides signals for the dashboard.
    The signals are used to create a dashboard for a user.

    """

    name = "lideresas.apps.dashboard"
    verbose_name = _("Dashboard")

    def ready(self):
        with contextlib.suppress(ImportError):
            import lideresas.apps.dashboard.signals  # noqa: F401
