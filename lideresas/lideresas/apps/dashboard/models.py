from django.core.exceptions import PermissionDenied
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from lideresas.apps.users.models import User


class Dashboard(models.Model):
    """Dashboard model.

    Description: This model represents a dashboard.

    Attributes:
        admin (OneToOneField): The admin of the dashboard.

    Methods:
        __str__ (Any): Returns the string representation of the dashboard.
        get_absolute_url (Any): Returns the absolute url of the dashboard.
        get_actions (Any): Returns the actions of the dashboard.
        clean (Any): Validates the dashboard.

    Example:
        >>> dashboard = Dashboard.objects.create(admin=user)
        >>> dashboard.admin
        <User: test>
        >>> dashboard.get_actions()
        <QuerySet [<DashboardAction: Test Action>]>
        >>> dashboard.get_absolute_url()
        '/dashboards/1/'

    Raises:
        PermissionDenied: Permission denied.

    """

    admin = models.OneToOneField(
        User,
        verbose_name=_(""),
        on_delete=models.CASCADE,
        related_name="dashboard",
    )

    class Meta:
        verbose_name = _("Dashboard")
        verbose_name_plural = _("Dashboards")

    def __str__(self):
        return self.admin.username

    def get_absolute_url(self):
        return reverse("dashboards:dashboard-detail", kwargs={"pk": self.pk})

    def get_actions(self) -> models.QuerySet:
        return self.dashboard_actions.all()

    def clean(self):
        if self.admin.is_superuser:
            return
        raise PermissionDenied


class DashboardAction(models.Model):
    """Dashboard action model.

    Description: This model represents a dashboard action.

    Attributes:
        dash_board (ForeignKey): The dashboard of the action.
        action_type (CharField): The type of the action.
        date (DateTimeField): The date of the action.
        description (TextField): The description of the action.

    Methods:
        __str__ (Any): Returns the string representation of the dashboard action.
        get_absolute_url (Any): Returns the absolute url of the dashboard action.

    Example:
        >>> dashboard_action = DashboardAction.objects.create(
        ...     dash_board=dashboard,
        ...     action_type="query",
        ...     date=datetime.now(),
        ...     description="This is a test dashboard action.",
        ... )
        >>> dashboard_action.get_absolute_url()

    Raises:
        PermissionDenied: Permission denied.
    """

    action_types = (
        ("query", _("Query")),
        ("warning", _("Warning")),
        ("ban", _("Ban")),
        ("delete", _("Delete")),
    )

    dash_board = models.ForeignKey(
        Dashboard,
        verbose_name=_(""),
        on_delete=models.CASCADE,
        related_name="dashboard_actions",
    )

    action_type = models.CharField(
        _("Action type"),
        choices=action_types,
        max_length=50,
    )

    date = models.DateTimeField(_("Action date"), auto_now_add=True)

    description = models.TextField(_("Description"), default="")

    class Meta:
        verbose_name = _("Dashboard action")
        verbose_name_plural = _("Dashboard actions")

    def __str__(self):
        return f"{self.dash_board} - {self.action_type} - {self.date}"

    def get_absolute_url(self):
        return reverse("DashboardAction_detail", kwargs={"pk": self.pk})
