from django.utils.translation import gettext_lazy as _
from django_filters import CharFilter
from django_filters import DateFilter
from django_filters import FilterSet
from django_filters import OrderingFilter

from lideresas.apps.users.models import User


class UserFilter(FilterSet):
    """User filter.

    Description: This filter is used to filter users.

    Attributes:
        username (CharFilter): The username filter.
        date_joined (DateFilter): The date joined filter.
        last_login (DateFilter): The last login filter.
        is_active (OrderingFilter): The is active filter.

    Methods:
        __init__ (Any): Initializes the filter.

    Example:
        >>> from lideresas.users.filters import UserFilter
        >>> filter = UserFilter()
        >>> filter.qs.all()
        <QuerySet [<User: admin>]>
        >>> filter.qs.count()
        1

    """

    username = CharFilter(lookup_expr="icontains", label=_("User username"))
    date_joined = DateFilter(lookup_expr="date", label=_("User data joined"))
    last_login = DateFilter(lookup_expr="date", label=_("User last login"))
    is_active = OrderingFilter(fields=("is_active",), label=_("User active"))

    class Meta:
        model = User
        fields = [
            "username",
            "date_joined",
            "last_login",
            "is_active",
        ]
