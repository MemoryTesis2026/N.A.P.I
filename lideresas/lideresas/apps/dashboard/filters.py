from django_filters import CharFilter
from django_filters import DateTimeFilter
from django_filters import FilterSet
from django_filters import OrderingFilter

from lideresas.apps.dashboard.models import DashboardAction


class DashboardActionFilter(FilterSet):
    """Dashboard action filter.

    Description: This filter is used to filter dashboard actions.

    Attributes:
        action_type (CharFilter): The action type filter.
        date (DateTimeFilter): The date filter.
        order_by (OrderingFilter): The order by filter.

    Methods:
        __init__ (Any): Initializes the filter.

    Example:
        >>> from lideresas.dashboard.filters import DashboardActionFilter
        >>> filter = DashboardActionFilter()
        >>> filter.qs.all()
        <QuerySet [<DashboardAction: Test Action>]>
        >>> filter.qs.count()
        1

    """

    action_type = CharFilter(
        field_name="action_type",
        label="Action type",
    )

    date = DateTimeFilter(
        field_name="date",
        label="Date",
    )

    order_by = OrderingFilter(
        fields=(("date", "Date"),),
    )

    class Meta:
        model = DashboardAction
        fields = (
            "action_type",
            "date",
        )
