from django.contrib import admin

from .models import Comuna
from .models import Location
from .models import Province
from .models import Region

admin.site.register(
    (
        Comuna,
        Location,
        Province,
        Region,
    ),
)
