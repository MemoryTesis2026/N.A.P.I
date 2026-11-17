from django import forms
from django.utils.translation import gettext_lazy as _

from lideresas.apps.locations.models import Comuna
from lideresas.apps.users.models import User

from .models import Organization


class OrganizationCreateForm(forms.ModelForm):
    """Organization create form.

    Description: This form is used to create a new organization.

    Attributes:
        owner (ModelChoiceField): The owner of the organization.
        organization_type (ModelChoiceField): The organization type of the organization.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.organizations.forms import OrganizationCreateForm
        >>> form = OrganizationCreateForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"name": "Test Organization", "owner": "test", "organization_type": "test"})
        True

    """

    owner = forms.ChoiceField(
        label=_("Organization owner"),
        choices=[],
        required=False,
        widget=forms.widgets.HiddenInput,
    )

    class Meta:
        model = Organization
        fields = ("name", "description", "owner", "organization_type")

    def __init__(self, *args, **kwargs):
        """Initializes the form.

        Description: This method is used to initialize the form.
            It adds the owner field to the form.
            It also adds the user to the form kwargs.

        Args:
            *args (Any): Additional arguments.
            **kwargs (Any): Additional keyword arguments.

        Raises:
            Http404: If the user is not found.
        """

        user = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["owner"] = forms.ModelChoiceField(
            queryset=User.objects.filter(pk=user.pk),
            widget=forms.HiddenInput,
        )


class OrganizationUpdateForm(forms.ModelForm):
    """Organization update form.

    Description: This form is used to update a organization.

    Attributes:
        name (CharField): The name of the organization.
        description (CharField): The description of the organization.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.organizations.forms import OrganizationUpdateForm
        >>> form = OrganizationUpdateForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"name": "Test Organization", "description": "Test Description"})
        True

    """

    class Meta:
        model = Organization
        fields = ("name", "description")


class OrganizationDeleteForm(forms.ModelForm):
    """Organization delete form.

    Description: This form is used to delete a organization.

    Attributes:
        confirmation (BooleanField): The confirmation field.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.organizations.forms import OrganizationDeleteForm
        >>> form = OrganizationDeleteForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"confirmation": True})
        True

    """

    confirmation = forms.BooleanField(label=_("Confirmation"), required=False)

    class Meta:
        model = Organization
        fields = ()


class OrganizationSetLocationForm(forms.Form):
    """Organization set location form.

    Description: This form is used to set the location of an organization.

    Attributes:
        organization (ModelChoiceField): The organization to set the location of.
        comuna (ModelChoiceField): The comuna to set the location of.
        street (CharField): The street to set the location of.
        number (IntegerField): The number to set the location of.

    Methods:
        __init__ (Any): Initializes the form.


    Example:
        >>> from lideresas.organizations.forms import OrganizationSetLocationForm
        >>> form = OrganizationSetLocationForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"comuna": "Test Comuna", "street": "Test Street", "number": "1"})
        True

    """

    organization = forms.ModelChoiceField(
        label=_("Organization"),
        queryset=Organization.objects.all(),
        widget=forms.widgets.HiddenInput,
    )
    comuna = forms.ModelChoiceField(label=_("Comuna"), queryset=Comuna.objects.all())
    street = forms.CharField(label=_("Street"), required=True, max_length=128)
    number = forms.IntegerField(label=_("Number"), required=True)
