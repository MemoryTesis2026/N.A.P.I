from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    """Region model.

    Description: This model represents a region.

    Attributes:
        name (CharField): The name of the region.
        cod (CharField): The code of the region.
        number (CharField): The number of the region.

    Example:
        >>> region = Region.objects.create(name="Region 1", cod="R1", number="1")
        >>> region.get_absolute_url()

    Methods:
        __str__ (str): Returns the string representation of the region.
        get_absolute_url (str): Returns the URL for the region.


    """

    name = models.CharField(_("Region name"), max_length=64, unique=True)
    cod = models.CharField(_("Region code"), max_length=32, unique=True)
    number = models.CharField(_("Region number"), max_length=32, unique=True)

    class Meta:
        ordering = ("number",)
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("region:detail", kwargs={"pk": self.pk})


class Province(models.Model):
    """Province model.

    Description: This model represents a province.

    Attributes:
        region (ForeignKey): The region of the province.
        name (CharField): The name of the province.
        cod (CharField): The code of the province.

    Methods:
        __str__ (str): Returns the string representation of the province.
        get_absolute_url (str): Returns the URL for the province.

    Example:
        >>> province = Province.objects.create(region=region, name="Province 1", cod="P1")
        >>> province.get_absolute_url()
        '/locations/1/provinces/1/'

    """

    region = models.ForeignKey(
        Region,
        verbose_name=_("Province region"),
        on_delete=models.CASCADE,
        related_name="cities",
    )
    name = models.CharField(_("Province name"), max_length=64, unique=True)
    cod = models.CharField(_("Province code"), max_length=32, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return f"{self.region} - {self.name}"

    def get_absolute_url(self):
        return reverse("city:detail", kwargs={"pk": self.pk})


class Comuna(models.Model):
    """Comuna model.

    Description: This model represents a comuna.

    Attributes:
        province (ForeignKey): The province of the comuna.
        name (CharField): The name of the comuna.
        cod (CharField): The code of the comuna.

    Methods:
        __str__ (str): Returns the string representation of the comuna.
        get_absolute_url (str): Returns the URL for the comuna.

    Example:
        >>> comuna = Comuna.objects.create(province=province, name="Comuna 1", cod="C1")
        >>> comuna.get_absolute_url()
        '/locations/1/comunas/1/'

    """

    province = models.ForeignKey(
        Province,
        verbose_name=_("Comuna province"),
        on_delete=models.CASCADE,
        related_name="comunas",
    )
    name = models.CharField(_("Comuna name"), max_length=64, unique=True)
    cod = models.CharField(_("Comuna code"), max_length=32, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Comuna")
        verbose_name_plural = _("Comunas")

    def __str__(self):
        return f"{self.province} - {self.name}"

    def get_absolute_url(self):
        return reverse("comuna:detail", kwargs={"pk": self.pk})


class Location(models.Model):
    """Location model.

    Description: This model represents a location.
        It is used to represent a location in a specific comuna.
        it has a street and a number.

    Attributes:
        comuna (ForeignKey): The comuna of the location.
        street (CharField): The street of the location.
        number (PositiveSmallIntegerField): The number of the location.

    Methods:
        __str__ (str): Returns the string representation of the location.
        get_absolute_url (str): Returns the URL for the location.

    Example:
        >>> location = Location.objects.create(comuna=comuna, street="Calle 1", number=1)
        >>> location.get_absolute_url()
        '/locations/1/'

    """

    comuna = models.ForeignKey(
        Comuna,
        verbose_name=_("Comuna"),
        on_delete=models.CASCADE,
        related_name="locations",
    )

    street = models.CharField(_("Street name"), max_length=96)
    number = models.PositiveSmallIntegerField(_("Street Number"))

    class Meta:
        verbose_name = _("Organization location")
        verbose_name_plural = _("Organization locations")

    def __str__(self):
        return f"{self.comuna} - {self.street}.{self.number}"

    def get_absolute_url(self):
        return reverse("location:detail", kwargs={"pk": self.pk})
