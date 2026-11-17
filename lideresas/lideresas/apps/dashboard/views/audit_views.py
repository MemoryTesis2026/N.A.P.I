from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.views.generic import DetailView
from django.views.generic import ListView

from lideresas.apps.dashboard.filters import DashboardActionFilter
from lideresas.apps.dashboard.models import DashboardAction


class DashboardAuditListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Dashboard audit list view.

    Description: This view is used to list the audits of a user.

    Attributes:
        model (DashboardAction): The model used to list the audits of a user.
        template_name (str): The template used to render the view.
        paginate_by (int): The number of items to be displayed per page.
        paginator_class (Paginator): The paginator class to be used in the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.

    """

    model = DashboardAction
    template_name = "dashboard/views/audit/dashboard_audit_list.html"
    paginate_by = 30
    paginator_class = Paginator

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        context["audit_filter"] = DashboardActionFilter(
            self.request.GET,
            queryset=DashboardAction.objects.all().order_by("-date"),
        )
        return context


dashboard_audit_list_view = DashboardAuditListView.as_view()


class DashboardAuditDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Dashboard audit detail view.

    Description: This view is used to display the details of an audit.

    Attributes:
        model (DashboardAction): The model used to display the details of an audit.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.

    """

    model = DashboardAction
    template_name = "dashboard/views/audit/dashboard_audit_detail.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        return context


dashboard_audit_detail_view = DashboardAuditDetailView.as_view()
