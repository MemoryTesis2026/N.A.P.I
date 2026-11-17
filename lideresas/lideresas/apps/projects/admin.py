from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Project
from .models import ProjectDocument
from .models import ProjectTransaction

admin.site.register(
    (
        Project,
        ProjectTransaction,
        ProjectDocument,
    ),
)
