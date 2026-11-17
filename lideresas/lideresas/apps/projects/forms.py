from django import forms
from django.utils.translation import gettext_lazy as _

from lideresas.apps.documents.forms import DocumentCreateForm
from lideresas.apps.locations.models import Comuna
from lideresas.apps.organizations.models import Organization
from lideresas.apps.users.models import User

from .models import Project
from .models import ProjectDocument
from .models import ProjectTransaction


class ProjectCreateForm(forms.ModelForm):
    """Project create form.

    Description: This form is used to create a new project.

    Example:
        >>> from lideresas.apps.projects.forms import ProjectCreateForm
        >>> form = ProjectCreateForm()
        >>> form.is_valid()
        False

    Attributes:
        owner (ModelChoiceField): The owner of the project.
        organization (ModelChoiceField): The organization of the project.

    Methods:
        __init__ (Any): Initializes the form.

    """

    class Meta:
        model = Project
        fields = (
            "name",
            "description",
            "state",
            "owner",
            "organization",
            "legal_representative",
            "legal_personality",
            "rut",
            "initial_balance",
        )

    def __init__(self, *args, **kwargs):
        """Initializes the form.

        Description: This method is used to initialize the form.
            It adds the owner and organization fields to the form.
            It also adds the user to the form kwargs.

        Args:
            *args (Any): Additional arguments.
            **kwargs (Any): Additional keyword arguments.

        Raises:
            Http404: If the user is not found.
        """

        user: User = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["owner"] = forms.ModelChoiceField(
            queryset=User.objects.filter(pk=user.pk),
            widget=forms.HiddenInput,
        )
        self.fields["organization"] = forms.ModelChoiceField(
            queryset=Organization.objects.filter(owner=user.pk),
        )


class ProjectSetLocationForm(forms.Form):
    """Project set location form.

    Description: This form is used to set the location of a project.

    Attributes:
        project (ModelChoiceField): The project to set the location of.
        comuna (ModelChoiceField): The comuna to set the location of.
        street (CharField): The street to set the location of.
        number (IntegerField): The number to set the location of.

    Methods:
        __init__ (Any): Initializes the form.

    """

    project = forms.ModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        widget=forms.widgets.HiddenInput,
    )
    comuna = forms.ModelChoiceField(label=_("Comuna"), queryset=Comuna.objects.all())
    street = forms.CharField(label=_("Street"), required=True)
    number = forms.IntegerField(label=_("Number"), required=True)


class ProjectUpdateForm(forms.ModelForm):
    """Project update form.

    Description: This form is used to update a project.

    Attributes:
        name (CharField): The name of the project.
        description (TextField): The description of the project.
        state (IntegerField): The state of the project.
        legal_representative (CharField): The legal representative of the project.
        legal_personality (CharField): The legal personality of the project.
        rut (CharField): The rut of the project.
        initial_balance (IntegerField): The initial balance of the project.

    Methods:
        __init__ (Any): Initializes the form.

    """

    class Meta:
        model = Project
        fields = (
            "name",
            "description",
            "state",
            "legal_representative",
            "legal_personality",
            "rut",
            "initial_balance",
        )


class ProjectDeleteForm(forms.ModelForm):
    """Project delete form.

    Description: This form is used to delete a project.

    Attributes:
        confirmation (BooleanField): The confirmation field.

    Methods:
        __init__ (Any): Initializes the form.

    """

    confirmation = forms.BooleanField(label=_("Confirmation"), required=False)

    class Meta:
        model = Project
        fields = ()


class ProjectDocumentCreateForm(DocumentCreateForm):
    """Project document create form.

    Description: This form is used to create a new document for a project.

    Attributes:
        document_type (ChoiceField): The document type of the document.
        project (ModelChoiceField): The project of the document.

    Methods:
        __init__ (Any): Initializes the form.

    """

    document_type = forms.ChoiceField(
        label=_("Document type"),
        choices=ProjectDocument.document_types[1:],
    )
    project = forms.ModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
    )

    class Meta:
        model = ProjectDocument
        fields = ("document_type", "name", "file", "project", "description")

    def __init__(self, *args, **kwargs):
        """Initializes the form.

        Description: This method is used to initialize the form.
            It adds the project field to the form.
            It also adds the user to the form kwargs.

        Args:
            *args (Any): Additional arguments.
            **kwargs (Any): Additional keyword arguments.

        Raises:
            Http404: If the user is not found.
        """

        user: User = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["project"] = forms.ModelChoiceField(
            label=_("Project"),
            queryset=Project.objects.filter(owner=user.pk),
        )


class ProjectDocumentUpdateForm(forms.ModelForm):
    """Project document update form.

    Description: This form is used to update a document of a project.

    Attributes:
        document_type (ChoiceField): The document type of the document.
        name (CharField): The name of the document.
        file (FileField): The file of the document.

    Methods:
        __init__ (Any): Initializes the form.

    """

    class Meta:
        model = ProjectDocument
        fields = ("document_type", "name", "file")


class ProjectDocumentDeleteForm(forms.ModelForm):
    """Project document delete form.

    Description: This form is used to delete a document of a project.

    Attributes:
        confirmation (BooleanField): The confirmation field.

    Methods:
        __init__ (Any): Initializes the form.

    """

    confirmation = forms.BooleanField(label=_("Confirmation"), required=False)

    class Meta:
        model = ProjectDocument
        fields = ()


class ProjectTransactionCreateForm(ProjectDocumentCreateForm):
    """Project transaction create form.

    Description: This form is used to create a new transaction for a project.

    Attributes:
        amount (IntegerField): The amount of the transaction.
        transaction_type (ChoiceField): The type of the transaction.

    Methods:
        __init__ (Any): Initializes the form.

    """

    document_type = forms.ChoiceField(
        label=_("Document type"),
        choices=ProjectDocument.document_types,
        # widget=forms.widgets.HiddenInput,
        initial="Boleta",
    )

    project = forms.ModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
    )

    class Meta:
        model = ProjectTransaction
        fields = ("amount", "transaction_type")

    def __init__(self, *args, **kwargs):
        """Initializes the form.

        Description: This method is used to initialize the form.
            It adds the project field to the form.
            It also adds the user to the form kwargs.

        Args:
            *args (Any): Additional arguments.
            **kwargs (Any): Additional keyword arguments.

        Raises:
            Http404: If the user is not found.
        """

        user: User = kwargs.get("user")
        super().__init__(*args, **kwargs)
        self.fields["project"] = forms.ModelChoiceField(
            label=_("Project"),
            queryset=Project.objects.filter(owner=user.pk),
            widget=forms.widgets.HiddenInput,
        )
        self.fields["document_type"] = forms.ChoiceField(
            label=_("document type"),
            choices=ProjectDocument.document_types[0:1],
            widget=forms.widgets.HiddenInput,
            initial="boleta",
        )

    def clean(self):
        """Clean the data.

        Description: This method is used to clean the data.
            It sets the project field to the cleaned data.

        Returns:
            dict[str, Any]: The cleaned data.
        """

        self.cleaned_data["project"] = self.data["project"]
        return super().clean()


class ProjectTransactionUpdateForm(forms.ModelForm):
    """Project transaction update form.

    Description: This form is used to update a transaction of a project.

    Attributes:
        amount (IntegerField): The amount of the transaction.
        transaction_type (ChoiceField): The type of the transaction.

    Methods:
        __init__ (Any): Initializes the form.

    """

    class Meta:
        model = ProjectTransaction
        fields = ()


class ProjectTransactionDeleteForm(forms.ModelForm):
    """Project transaction delete form.

    Description: This form is used to delete a transaction of a project.

    Attributes:
        confirmation (BooleanField): The confirmation field.

    Methods:
        __init__ (Any): Initializes the form.

    """

    confirmation = forms.BooleanField(label=_("Confirmation"), required=False)

    class Meta:
        model = ProjectTransaction
        fields = ()
