from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Document


class DocumentCreateForm(forms.ModelForm):
    """Document create form.

    Description: This form is used to create a new document.

    Attributes:
        name (CharField): The name of the document.
        description (CharField): The description of the document.
        file (FileField): The file of the document.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.documents.forms import DocumentCreateForm
        >>> form = DocumentCreateForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"name": "Test Document", "file": "test.pdf"})
        True

    """

    file = forms.FileField(
        label=_("File"),
        max_length=196,
        required=True,
        allow_empty_file=False,
    )

    class Meta:
        model: Document = Document
        fields = ("name", "description", "file")


class DocumentUpdateForm(forms.ModelForm):
    """Document update form.

    Description: This form is used to update a document.

    Attributes:
        name (CharField): The name of the document.
        description (CharField): The description of the document.
        file (FileField): The file of the document.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.documents.forms import DocumentUpdateForm
        >>> form = DocumentUpdateForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"name": "Test Document", "file": "test.pdf"})
        True

    """

    class Meta:
        model = Document
        fields = ("name", "description", "file")


class DocumentDeleteForm(forms.ModelForm):
    """Document delete form.

    Description: This form is used to delete a document.

    Attributes:
        confirmation (BooleanField): The confirmation field.

    Methods:
        __init__ (Any): Initializes the form.

    Example:
        >>> from lideresas.documents.forms import DocumentDeleteForm
        >>> form = DocumentDeleteForm()
        >>> form.is_valid()
        False
        >>> form.is_valid(data={"confirmation": True})
        True

    """

    confirmation = forms.BooleanField(label=_("Confirmation"), required=False)

    class Meta:
        model = Document
        fields = ()
