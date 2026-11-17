from django.contrib import admin

from .models import Dashboard
from .models import DashboardAction

admin.site.register(Dashboard)
admin.site.register(DashboardAction)
