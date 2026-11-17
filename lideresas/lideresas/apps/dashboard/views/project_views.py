from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from lideresas.apps.dashboard.models import DashboardAction
from lideresas.apps.projects.filters import ProjectDocumentFilter
from lideresas.apps.projects.filters import ProjectFilter
from lideresas.apps.projects.filters import ProjectTransactionFilter
from lideresas.apps.projects.forms import ProjectUpdateForm
from lideresas.apps.projects.models import Project
from lideresas.apps.projects.models import ProjectDocument
from lideresas.apps.projects.models import ProjectTransaction


class DashboardProjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Dashboard project list view.

    Description: This view is used to list the projects of a user.

    Attributes:
        model (Project): The model used to list the projects of a user.
        template_name (str): The template used to render the view.
        paginate_by (int): The number of items to be displayed per page.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.

    """

    model = Project
    template_name = "dashboard/views/projects/dashboard_project_list.html"
    paginate_by = 30

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        context["project_filter"] = ProjectFilter(
            self.request.GET,
            queryset=Project.objects.all(),
        )
        return context


dashboard_project_list_view = DashboardProjectListView.as_view()


class DashboardProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Dashboard project detail view.

    Description: This view is used to display the details of a project.

    Attributes:
        model (Project): The model used to display the details of a project.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.

    """

    model = Project
    template_name = "dashboard/views/projects/dashboard_project_detail.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        context["project_document_filter"] = ProjectDocumentFilter(
            self.request.GET,
            queryset=ProjectDocument.objects.all(),
        )
        context["project_transaction_filter"] = ProjectTransactionFilter(
            self.request.GET,
            queryset=ProjectTransaction.objects.all(),
        )
        return context


dashboard_project_detail_view = DashboardProjectDetailView.as_view()


class DashboardProjectUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    """Dashboard project update view.

    Description: This view is used to update a project.

    Attributes:
        model (Project): The model used to update a project.
        template_name (str): The template used to render the view.
        form_class (ProjectUpdateForm): The form used to update a project.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.
        get_initial (Any): Returns the initial data to be used in the form.
        form_valid (Any): Updates the project.

    """

    model = Project
    template_name = "dashboard/views/projects/dashboard_project_update.html"
    form_class = ProjectUpdateForm

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        return context

    def get_initial(self):
        return {
            "project": self.object,
        }

    def form_valid(self, form):
        new_log = DashboardAction(
            action_type="update",
            dash_board=self.request.user.dashboard,
            description=f"Project {self.object.name} updated",
        )
        new_log.save()
        return super().form_valid(form)


dashboard_project_update_view = DashboardProjectUpdateView.as_view()


class DashboardProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Dashboard project delete view.

    Description: This view is used to delete a project.

    Attributes:
        model (Project): The model used to delete a project.
        template_name (str): The template used to render the view.
        form_class (ProjectDeleteForm): The form used to delete a project.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_success_url (str): Returns the URL to redirect to after the project is deleted.
        get_initial (Any): Returns the initial data to be used in the form.
        get_form_kwargs (Any): Returns the form kwargs to be used in the form.

    """

    model = Project
    template_name = "dashboard/views/projects/dashboard_project_delete.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """Get the context data.

        Description: This method is used to get the context data.
            It calls the superclass method to get the context data.
            It adds the project to the context data.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: The context data.

        """

        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard

        return context

    def delete(self, request, *args, **kwargs):
        """Delete the project.

        Description: This method is used to delete the project.
            It calls the superclass method to delete the project.
            It creates a new log for the project.

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
            description=f"Project {self.object.name} deleted",
        )
        new_log.save()
        return super().delete(request, *args, **kwargs)


dashboard_project_delete_view = DashboardProjectDeleteView.as_view()
