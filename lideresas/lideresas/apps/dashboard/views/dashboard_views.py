from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView

from lideresas.apps.dashboard.models import Dashboard
from lideresas.apps.dashboard.models import DashboardAction
from lideresas.apps.organizations.models import Organization
from lideresas.apps.projects.models import Project
from lideresas.apps.projects.models import ProjectDocument


class DashboardIndexView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Dashboard index view.

    Description: This view is used to display the dashboard of a user.

    Attributes:
        model (Dashboard): The model used to display the dashboard of a user.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_object (Any): Returns the object to be used in the view.

    """

    model = Dashboard
    template_name = "dashboard/views/dashboard_detail.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_object(self):
        assert self.request.user.is_authenticated
        return self.request.user.dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["stats"] = {
            "projects": Project.objects.all().count(),
            "organizations": Organization.objects.all().count(),
            "documents": ProjectDocument.objects.all().count(),
        }
        context["logs"] = DashboardAction.objects.all().order_by("-date")
        return context


dashboard_detail_view = DashboardIndexView.as_view()
