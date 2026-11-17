from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet
from django_filters import filters

from lideresas.apps.locations.models import Comuna
from lideresas.apps.locations.models import Province
from lideresas.apps.locations.models import Region
from lideresas.apps.locations.tasks import get_values_for_filter
from lideresas.apps.organizations.models import Organization
from lideresas.apps.organizations.models import OrganizationType


class OrganizationFilter(FilterSet):
    """Organization filter.

    Description: This filter is used to filter organizations.

    Attributes:
        name (CharField): The name of the organization.
        description (CharField): The description of the organization.
        owner (CharField): The owner of the organization.
        organization_type (CharField): The organization type of the organization.
        location__comuna (CharField): The comuna of the location of the organization.
        location__comuna__province (CharField): The province of the location of the organization.
        location__comuna__province__region (CharField): The region of the location of the organization.

    Todo: Cache system for comuna, province and region.

    Methods:
        __init__ (Any): Initializes the filter.

    Example:
        >>> from lideresas.organizations.filters import OrganizationFilter
        >>> filter = OrganizationFilter()
        >>> filter.qs.all()
        <QuerySet [<Organization: Test Organization>]>
        >>> filter.qs.count()
        1

    """

    name = filters.CharFilter(
        lookup_expr="icontains",
        field_name="name",
        label=_("Organization name"),
    )

    owner = filters.CharFilter(
        lookup_expr="icontains",
        field_name="owner__name",
        label=_("Organization owner name"),
    )

    organization_type = filters.ChoiceFilter(
        choices=lambda: get_values_for_filter(
            OrganizationType,
            ("name", "name"),
            first_empty=True,
        ),
        label=_("Organization type"),
        lookup_expr="icontains",
        field_name="organization_type__name",
        null_label=None,
        empty_label=None,
    )
    comuna = filters.ChoiceFilter(
        choices=lambda: get_values_for_filter(
            Comuna,
            ("name", "name"),
            first_empty=True,
        ),
        label=_("Organization comuna"),
        lookup_expr="icontains",
        field_name="location__comuna__name",
        null_label=None,
        empty_label=None,
    )

    province = filters.ChoiceFilter(
        choices=lambda: get_values_for_filter(
            Province,
            ("name", "name"),
            first_empty=True,
        ),
        label=_("Organization province"),
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
        label=_("Organization region"),
        lookup_expr="icontains",
        field_name="location__comuna__province__region__name",
        null_label=None,
        empty_label=None,
    )

    class Meta:
        model = Organization
        fields = [
            "name",
            "owner",
        ]


class OrganizationTypeFilter(FilterSet):
    """Organization type filter.

    Description: This filter is used to filter organization types.

    Attributes:
        name (CharField): The name of the organization type.
        description (CharField): The description of the organization type.

    Methods:
        __init__ (Any): Initializes the filter.

    Example:
        >>> from lideresas.organizations.filters import OrganizationTypeFilter
        >>> filter = OrganizationTypeFilter()
        >>> filter.qs.all()
        <QuerySet [<OrganizationType: Test Organization Type>]>
        >>> filter.qs.count()
        1

    """

    class Meta:
        model = OrganizationType
        fields = {
            "name": ["exact", "icontains"],
            "description": ["exact", "icontains"],
        }
