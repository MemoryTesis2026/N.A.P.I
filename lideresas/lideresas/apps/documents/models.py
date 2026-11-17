from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from lideresas.apps.documents.fields import ContentTypeRestrictedFileField


class Document(models.Model):
    """Document model.

    Description: This model represents a document.

    Attributes:
        name (CharField): The name of the document.
        description (TextField): The description of the document.
        upload_at (DateTimeField): The date and time when the document was uploaded.
        edit_at (DateTimeField): The date and time when the document was edited.
        file (FileField): The file of the document.

    Methods:
        __str__ (str): Returns the string representation of the document.
        get_absolute_url (str): Returns the URL for the document.

    Example:
        >>> from lideresas.documents.models import Document
        >>> document = Document.objects.create(name="Test Document", file="test.pdf")
        >>> document.name
        'Test Document'
        >>> document.file
        <ContentTypeRestrictedFile: test.pdf>
        >>> document.get_absolute_url()
        '/documents/1/'

    """

    name = models.CharField(
        _("Document name"),
        max_length=64,
        default="",
    )

    description = models.TextField(
        _("Document description"),
        max_length=1024,
        default="",
    )

    upload_at = models.DateTimeField(
        _("Uploaded at"),
        auto_now=False,
        auto_now_add=True,
    )

    edit_at = models.DateTimeField(_("Edited at"), auto_now=True, auto_now_add=False)

    file = ContentTypeRestrictedFileField(
        _("File"),
        upload_to="documents/",
        null=True,
        content_types=[
            "application/pdf",
            "text/plain",
            "image/jpeg",
            "image/png",
            "image/gif",
            "application/msword",
        ],
        max_upload_size=10485760,
        blank=True,
    )

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("documents:document-detail", kwargs={"pk": self.pk})

    @cached_property
    def get_display_name(self) -> str:
        """Get the display name of the document.

        Description: This method is used to get the display name of the document.
            It returns the last part of the file name.

        Returns:
            str: The display name of the document.
        """

        return self.file.split["/"][-1]
