import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    """ProjectsConfig class.

    The projects app is for managing projects. It provides models for projects,
    project documents, project transactions, and project transactions.

    """

    name = "lideresas.apps.projects"
    verbose_name = _("Projects")

    def ready(self):
        with contextlib.suppress(ImportError):
            import lideresas.apps.projects.signals  # noqa: F401
