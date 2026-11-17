from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet
from django_filters import filters

from lideresas.apps.locations.models import Comuna
from lideresas.apps.locations.models import Province
from lideresas.apps.locations.models import Region
from lideresas.apps.locations.tasks import get_values_for_filter
from lideresas.apps.projects.models import Project
from lideresas.apps.projects.models import ProjectDocument
from lideresas.apps.projects.models import ProjectTransaction


class ProjectFilter(FilterSet):
    """Project filter.

    Description: This filter is used to filter projects.

    Attributes:
        name (CharField): The name of the project.
        description (CharField): The description of the project.
        owner (CharField): The owner of the project.
        organization (CharField): The organization of the project.
        legal_representative (CharField): The legal representative of the project.
        legal_personality (CharField): The legal personality of the project.
        rut (CharField): The rut of the project.
        location__comuna (CharField): The comuna of the location of the project.
        location__comuna__province (CharField): The province of the location of the project.
        location__comuna__province__region (CharField): The region of the location of the project.

    Methods:
        __init__ (Any): Initializes the filter.

    Example:
        >>> from lideresas.projects.filters import ProjectFilter
        >>> filter = ProjectFilter()
        >>> filter.qs.all()
        <QuerySet [<Project: Test Project>]>
        >>> filter.qs.count()
        1

    """

    name = filters.CharFilter(
        lookup_expr="icontains",
        field_name="name",
        label=_("Project name"),
    )

    owner = filters.CharFilter(
        lookup_expr="icontains",
        field_name="owner__name",
        label=_("Project owner name"),
    )

    legal_representative = filters.CharFilter(
        lookup_expr="icontains",
        field_name="legal_representative",
        label=_("Project legal representative"),
    )

    legal_personality = filters.CharFilter(
        lookup_expr="icontains",
        field_name="legal_personality",
        label=_("Project legal personality"),
    )

    rut = filters.CharFilter(
        lookup_expr="icontains",
        field_name="rut",
        label=_("Project rut"),
    )

    comuna = filters.ChoiceFilter(
        choices=lambda: get_values_for_filter(
            Comuna,
            ("name", "name"),
            first_empty=True,
        ),
        lookup_expr="icontains",
        field_name="location__comuna__name",
        label=_("Project comuna"),
        null_label=None,
        empty_label=None,
    )

    province = filters.ChoiceFilter(
        choices=lambda: get_values_for_filter(
            Province,
            ("name", "name"),
            first_empty=True,
        ),
        label=_("Project province"),
        lookup_expr="icontains",
        field_name="location__comuna__province__name",
        null_label=None,
        empty_label=None,
    )

    region = filters.ChoiceFilter(
        choices=lambda: get_values_for_filter(
            Region,
            ("name", "name"),
            first_empty=True,
        ),
        label=_("Project region"),
        lookup_expr="icontains",
        field_name="location__comuna__province__region__name",
        null_label=None,
        empty_label=None,
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "owner",
            "organization",
            "legal_representative",
            "legal_personality",
            "rut",
        ]


class ProjectDocumentFilter(FilterSet):
    """Project document filter.

    Description: This filter is used to filter project documents.

    Attributes:
        name (CharField): The name of the project document.
        description (CharField): The description of the project document.
        document_type (CharField): The document type of the project document.

    Methods:
        __init__ (Any): Initializes the filter.

    Example:
        >>> from lideresas.projects.filters import ProjectDocumentFilter
        >>> filter = ProjectDocumentFilter()
        >>> filter.qs.all()
        <QuerySet [<ProjectDocument: Test Document>]>
        >>> filter.qs.count()
        1

    """

    class Meta:
        model = ProjectDocument
        fields = {
            "name": ["exact", "icontains"],
            "description": ["exact", "icontains"],
            "document_type": ["exact", "icontains"],
            "project__name": ["exact", "icontains"],
        }


class ProjectTransactionFilter(FilterSet):
    """Project transaction filter.

    Description: This filter is used to filter project transactions.

    Attributes:
        name (CharField): The name of the project transaction.
        description (CharField): The description of the project transaction.
        balance (CharField): The balance of the project transaction.

    Methods:
        __init__ (Any): Initializes the filter.

    Example:
        >>> from lideresas.projects.filters import ProjectTransactionFilter
        >>> filter = ProjectTransactionFilter()
        >>> filter.qs.all()
        <QuerySet [<ProjectTransaction: Test Transaction>]>
        >>> filter.qs.count()
        1

    """

    class Meta:
        model = ProjectTransaction
        fields = {
            "name": ["exact", "icontains"],
            "description": ["exact", "icontains"],
            "balance": ["exact", "gt", "lt", "gte", "lte"],
        }
