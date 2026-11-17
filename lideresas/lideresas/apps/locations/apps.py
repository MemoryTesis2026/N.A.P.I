import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsConfig(AppConfig):
    """LocationsConfig class.
    The locations app is for managing locations. It provides models for locations,
    provinces, regions, and comunas.

    """

    name = "lideresas.apps.locations"
    verbose_name = _("Locations")

    def ready(self):
        with contextlib.suppress(ImportError):
            import lideresas.apps.locations.signals  # noqa: F401
