from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from lideresas.apps.dashboard.models import DashboardAction
from lideresas.apps.organizations.filters import OrganizationFilter
from lideresas.apps.organizations.filters import OrganizationTypeFilter
from lideresas.apps.organizations.forms import OrganizationUpdateForm
from lideresas.apps.organizations.models import Organization
from lideresas.apps.organizations.models import OrganizationType


class DashboardOrganizationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Dashboard organization list view.

    Description: This view is used to list the organizations of a user.

    Attributes:
        model (Organization): The model used to list the organizations of a user.
        template_name (str): The template used to render the view.
        paginate_by (int): The number of items to be displayed per page.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.

    """

    model = Organization
    template_name = "dashboard/views/organization/dashboard_organization_list.html"
    paginate_by = 30

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        assert self.request.user.is_authenticated
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        context["organization_filter"] = OrganizationFilter(
            self.request.GET,
            queryset=Organization.objects.all(),
        )
        return context


dashboard_organization_list_view = DashboardOrganizationListView.as_view()


class DashboardOrganizationDetailView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DetailView,
):
    """Dashboard organization detail view.

    Description: This view is used to display the details of an organization.

    Attributes:
        model (Organization): The model used to display the details of an organization.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.

    """

    model = Organization
    template_name = "dashboard/views/organization/dashboard_organization_detail.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        context["organization_type_filter"] = OrganizationTypeFilter(
            self.request.GET,
            queryset=OrganizationType.objects.all(),
        )
        return context


dashboard_organization_detail_view = DashboardOrganizationDetailView.as_view()


class DashboardOrganizationUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    """Dashboard organization update view.

    Description: This view is used to update an organization.

    Attributes:
        model (Organization): The model used to update an organization.
        template_name (str): The template used to render the view.
        form_class (OrganizationUpdateForm): The form used to update an organization.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.
        get_initial (Any): Returns the initial data to be used in the form.
        form_valid (Any): Updates the organization.

    """

    model = Organization
    template_name = "dashboard/views/organization/dashboard_organization_update.html"
    form_class = OrganizationUpdateForm

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        return context

    def get_initial(self):
        return {
            "organization": self.object,
        }

    def form_valid(self, form):
        """Update the organization.

        Description: This method is used to update the organization.
            It creates a new log for the organization.

        Args:
            form (OrganizationUpdateForm): The form used to update the organization.

        Returns:
            HttpResponse: The response to be returned.

        """

        new_log = DashboardAction(
            action_type="update",
            dash_board=self.request.user.dashboard,
            description=f"Organization {self.object.name} updated",
        )
        new_log.save()
        return super().form_valid(form)


dashboard_organization_update_view = DashboardOrganizationUpdateView.as_view()


class DashboardOrganizationDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    """Dashboard organization delete view.

    Description: This view is used to delete an organization.

    Attributes:
        model (Organization): The model used to delete an organization.
        template_name (str): The template used to render the view.
        form_class (OrganizationDeleteForm): The form used to delete an organization.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_success_url (str): Returns the URL to redirect to after the organization is deleted.
        get_initial (Any): Returns the initial data to be used in the form.
        get_form_kwargs (Any): Returns the form kwargs to be used in the form.

    """  # noqa: E501

    model = Organization
    template_name = "dashboard/views/organization/dashboard_organization_delete.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """Get the context data.

        Description: This method is used to get the context data.
            It calls the superclass method to get the context data.
            It adds the organization to the context data.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: The context data.

        """

        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard

        return context

    def delete(self, request, *args, **kwargs):
        """Delete the organization.

        Description: This method is used to delete the organization.
            It calls the superclass method to delete the organization.
            It creates a new log for the organization.

        Args:
            request (HttpRequest): The request.
            *args (Any): Additional arguments.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            HttpResponse: The response to be returned.

        """
        new_log = DashboardAction(
            action_type="delete",
            dash_board=self.request.user.dashboard,
            description=f"Organization {self.object.name} deleted",
        )
        new_log.save()
        return super().delete(request, *args, **kwargs)


dashboard_organization_delete_view = DashboardOrganizationDeleteView.as_view()
