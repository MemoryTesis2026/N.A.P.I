from collections.abc import Iterable

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from lideresas.apps.balances.models import Balance
from lideresas.apps.balances.models import BalanceTransaction
from lideresas.apps.documents.models import Document
from lideresas.apps.locations.models import Location
from lideresas.apps.organizations.models import Organization
from lideresas.apps.users.models import User


class Project(Balance):
    """Project model.

    Description: This model represents a project.

    Attributes:
        name (CharField): The name of the project.
        descipcion (TextField): The description of the project.
        indicador (BooleanField): The indicator of success of the project.
        location (ForeignKey): The location of the project.
        owner (ForeignKey): The owner of the project.
        organization (ForeignKey): The organization of the project.
        legal_representative (CharField): The legal representative of the project.
        legal_personality (CharField): The legal personality of the project.
        rut (CharField): The rut of the project.

    Methods:
        __str__ (str): Returns the string representation of the project.
        get_absolute_url (str): Returns the URL for the project.
        get_all_documents (QuerySet): Returns all the documents of the project.
        get_all_boletas (QuerySet): Returns all the boletas of the project.

    Example:
        >>> from lideresas.project.models import Project
        >>> project = Project.objects.create(name="Test Project")
        >>> project.name
        'Test Project'

    """

    indicators = [
        (3, _("Canceled")),
        (2, _("In progress")),
        (1, _("Successful")),
        (0, _("Failed")),
    ]
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=512, default="")

    state = models.IntegerField(
        _("State"),
        choices=indicators,
        default=0,
    )
    location = models.ForeignKey(
        Location,
        verbose_name=_("Location"),
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_("Owner"),
        on_delete=models.CASCADE,
        related_name="projects",
    )

    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
    )

    legal_representative = models.CharField(
        _("Legal Representative"),
        max_length=128,
        default="",
    )
    legal_personality = models.CharField(
        _("Legal Personality"),
        max_length=255,
        default="",
    )
    rut = models.CharField(
        _("RUT"),
        max_length=255,
        default="",
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["rut"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.rut}"

    def get_absolute_url(self):
        return reverse("projects:project-detail", kwargs={"pk": self.pk})

    def get_all_documents(self) -> models.QuerySet:
        return self.project_documents.all()

    def get_all_boletas(self) -> Iterable:
        """Get all the boletas of the project.

        Description: This method is used to get all the boletas of the project.
            It filters the project documents to include only the boletas.

        Returns:
            Iterable: The boletas of the project.
        """

        return list(
            filter(lambda x: x.document_type == "boleta", self.project_documents.all()),
        )


class ProjectDocument(Document):
    """ProjectDocument model.

    Description: This model represents a document of a project.

    Attributes:
        name (CharField): The name of the document.
        description (TextField): The description of the document.
        upload_at (DateTimeField): The date and time when the document was uploaded.
        edit_at (DateTimeField): The date and time when the document was edited.
        file (FileField): The file of the document.
        project (ForeignKey): The project of the document.

    Methods:
        __str__ (str): Returns the string representation of the document.
        get_absolute_url (str): Returns the URL for the document.

    Example:
        >>> from lideresas.project.models import Project
        >>> from lideresas.document.models import Document
        >>> project = Project.objects.create(name="Test Project")
        >>> document = Document.objects.create(name="Test Document", project=project)
        >>> document.name
        'Test Document'
        >>> document.project
        <Project: Test Project>

    """

    document_types = (
        ("invoice", _("Invoice")),
        ("signature", _("Signature")),
        ("image", _("Image")),
        ("misc", _("Misc")),
    )
    document_type = models.CharField(
        _("Document type"),
        choices=document_types,
        max_length=32,
        default="misc",
    )
    project = models.ForeignKey(
        Project,
        verbose_name=_("Project"),
        on_delete=models.CASCADE,
        related_name="project_documents",
    )

    class Meta:
        verbose_name = _("Project Document")
        verbose_name_plural = _("Project Documents")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["document_type"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.document_type}"

    def get_absolute_url(self):
        return reverse("projects:document-detail", kwargs={"pk": self.pk})

    def get_file_name_display(self):
        return self.file.name.split("-")[-1]


class ProjectTransaction(ProjectDocument, BalanceTransaction):
    """ProjectTransaction model.

    Description: This model represents a transaction of a project.

    Attributes:
        balance (ForeignKey): The balance of the transaction.
        project (ForeignKey): The project of the transaction.

    Indexes:
        name (CharField): The name of the transaction.
        balance (ForeignKey): The balance of the transaction.

    Methods:
        __str__ (str): Returns the string representation of the transaction.
        get_absolute_url (str): Returns the URL for the transaction.

    Example:
        >>> from lideresas.project.models import Project
        >>> from lideresas.transaction.models import Transaction
        >>> project = Project.objects.create(name="Test Project")
        >>> transaction = Transaction.objects.create(name="Test Transaction", balance=project)
        >>> transaction.name
        'Test Transaction'
        >>> transaction.balance
        <Project: Test Project>

    """

    balance = models.ForeignKey(
        Project,
        verbose_name=_("Balance"),
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    class Meta:
        verbose_name = _("ProjectTransaction")
        verbose_name_plural = _("ProjectTransactions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:transaction-detail", kwargs={"pk": self.pk})
