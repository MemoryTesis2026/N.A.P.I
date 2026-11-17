from collections.abc import Iterable
from functools import cache

from django.db.models import Model


@cache
def get_values_for_filter(
    model: Model,
    fields: tuple[str],
    first_empty: bool = False,
) -> Iterable[tuple[str]]:
    """Get values for filter.

    Description: This function is used to get values for filter.

    Args:
        model (Model): The model to get values for.
        fields (list[str]): The fields to get values for.
        first_empty (bool, optional): Whether to return the first empty value or not. Defaults to False.

    Returns:
        list[str]: The values for filter.

    Example:
        >>> from lideresas.utils import get_values_for_filter
        >>> get_values_for_filter(model=User, fields=["username", "email"])
        [('admin', 'admin@example.com'), ('user1', 'user1@example.com'), ('user2', 'user2@example.com')]

    """
    values = model.objects.all().values_list(*fields, flat=False)
    if first_empty:
        values: list[tuple[str, str]] = list(values)
        values.insert(0, ("", ""))
    return values
