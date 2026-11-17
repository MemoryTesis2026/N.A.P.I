from django import forms
from django.utils.translation import gettext_lazy as _

from .models import DashboardAction


class DashboardActionCreateForm(forms.ModelForm):
    """Dashboard action create form.

    Description: This form is used to create a new dashboard action.

    Attributes:
        action_type (ChoiceField): The type of the action.
        date (DateTimeField): The date of the action.

    Methods:
        __init__ (Any): Initializes the form.


    Example:
        >>> from lideresas.dashboard.forms import DashboardActionCreateForm
        >>> form = DashboardActionCreateForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"action_type": "test", "date": "2023-01-01T00:00:00"})
        True

    """

    action_type = forms.ChoiceField(
        label=_("Action type"),
        choices=DashboardAction.action_types,
    )

    date = forms.DateTimeField(label=_("Action date"), required=True)

    class Meta:
        model = DashboardAction
        fields = ("action_type", "date")


class DashboardActionUpdateForm(forms.ModelForm):
    """Dashboard action update form.

    Description: This form is used to update a dashboard action.

    Attributes:
        action_type (ChoiceField): The type of the action.
        date (DateTimeField): The date of the action.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.dashboard.forms import DashboardActionUpdateForm
        >>> form = DashboardActionUpdateForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"action_type": "test", "date": "2023-01-01T00:00:00"})
        True

    """

    class Meta:
        model = DashboardAction
        fields = ("action_type", "date")


class DashboardActionDeleteForm(forms.ModelForm):
    """Dashboard action delete form.

    Description: This form is used to delete a dashboard action.

    Attributes:
        confirmation (BooleanField): The confirmation field.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.dashboard.forms import DashboardActionDeleteForm
        >>> form = DashboardActionDeleteForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"confirmation": True})
        True

    """

    confirmation = forms.BooleanField(label=_("Confirmation"), required=False)

    class Meta:
        model = DashboardAction
        fields = ()
