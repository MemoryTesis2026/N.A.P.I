import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentsConfig(AppConfig):
    """DocumentsConfig class.

    The documents app is for managing documents. It provides models for documents,
    document types, document categories, and document categories.

    """

    name = "lideresas.apps.documents"
    verbose_name = _("Documents")

    def ready(self):
        with contextlib.suppress(ImportError):
            import lideresas.apps.documents.signals  # noqa: F401
