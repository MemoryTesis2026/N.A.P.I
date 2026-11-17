from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Location


class LocationCreateForm(forms.ModelForm):
    """Location create form.

    Description: This form is used to create a new location.

    Attributes:
        comuna (ChoiceField): The comuna of the location.
        street (CharField): The street of the location.
        number (CharField): The number of the location.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.locations.forms import LocationCreateForm
        >>> form = LocationCreateForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"comuna": "Test Comuna", "street": "Test Street", "number": "1"})
        True
    """

    class Meta:
        model = Location
        fields = ()


class LocationUpdateForm(forms.ModelForm):
    """Location update form.

    Description: This form is used to update a location.

    Attributes:
        comuna (ChoiceField): The comuna of the location.
        street (CharField): The street of the location.
        number (CharField): The number of the location.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.locations.forms import LocationUpdateForm
        >>> form = LocationUpdateForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"comuna": "Test Comuna", "street": "Test Street", "number": "1"})
        True
    """

    class Meta:
        model = Location
        fields = ("pk",)


class LocationDeleteForm(forms.ModelForm):
    """Location delete form.

    Description: This form is used to delete a location.

    Attributes:
        confirmation (BooleanField): The confirmation field.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.locations.forms import LocationDeleteForm
        >>> form = LocationDeleteForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"confirmation": True})
        True
    """

    confirmation = forms.BooleanField(label=_("Confirmation"), required=False)

    class Meta:
        model = Location
        fields = ("pk",)
