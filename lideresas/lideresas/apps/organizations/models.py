from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from lideresas.apps.locations.models import Location
from lideresas.apps.users.models import User


class OrganizationType(models.Model):
    """Organization type model.

    Description: This model represents an organization type.

    Attributes:
        slug (CharField): The slug of the organization type.
        name (CharField): The name of the organization type.
        description (TextField): The description of the organization type.

    Methods:
        __str__ (str): Returns the string representation of the organization type.
        get_absolute_url (str): Returns the URL for the organization type.

    Example:
        >>> organization_type = OrganizationType.objects.create(name="Test Organization Type",
          description="This is a test organization type.")
        >>> organization_type.get_absolute_url()
        '/organization_type/1/'

    """

    slug = models.CharField(_("Slug organization type"), max_length=64, unique=True)
    name = models.CharField(_("Name organization type"), max_length=64, null=False)
    description = models.TextField(
        _("Description organization type"),
        max_length=1024,
        default="",
    )

    class Meta:
        verbose_name = _("Organization type")
        verbose_name_plural = _("Organization types")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization_type:detail", kwargs={"pk": self.pk})


class Organization(models.Model):
    """Organization model.

    Description: This model represents an organization.

    Attributes:
        name (CharField): The name of the organization.
        description (CharField): The description of the organization.
        owner (ForeignKey): The owner of the organization.
        organization_type (ForeignKey): The organization type of the organization.
        location (ForeignKey): The location of the organization.

    Methods:
        __str__ (str): Returns the string representation of the organization.
        get_absolute_url (str): Returns the URL for the organization.

    Example:
        >>> organization = Organization.objects.create(name="Test Organization",
            owner=user, organization_type=organization_type)
        >>> organization.get_absolute_url()
        '/organizations/1/'

    """

    name = models.CharField(_("Organization Name"), max_length=128, unique=True)
    description = models.CharField(
        _("Organization description"),
        max_length=512,
        default="",
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_("Owner"),
        on_delete=models.CASCADE,
        related_name="organizations",
    )
    organization_type = models.ForeignKey(
        OrganizationType,
        verbose_name=_("Organization type"),
        on_delete=models.CASCADE,
        related_name="organizations",
    )
    location = models.ForeignKey(
        Location,
        verbose_name=_("Location"),
        on_delete=models.CASCADE,
        related_name="organizations",
        null=True,
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return f"{self.name} - {self.organization_type.name}"

    def get_absolute_url(self):
        return reverse("organizations:organization-detail", kwargs={"pk": self.pk})

    def get_all_projects(self):
        return self.projects.all()
