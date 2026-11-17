from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from lideresas.apps.dashboard.models import DashboardAction
from lideresas.apps.users.filters import UserFilter
from lideresas.apps.users.forms import UserUpdateForm
from lideresas.apps.users.models import User


class DashboardUsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Dashboard users list view.

    Description: This view is used to list the users of a user.

    Attributes:
        model (User): The model used to list the users of a user.
        template_name (str): The template used to render the view.
        paginate_by (int): The number of items to be displayed per page.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.

    """

    model = User
    template_name = "dashboard/views/users/dashboard_users_list.html"
    paginate_by = 30

    def get_queryset(self):
        return User.objects.filter(username__isnull=False, id__isnull=False)

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        context["user_filter"] = UserFilter(
            self.request.GET,
            queryset=self.get_queryset(),
        )
        return context


dashboard_users_list_view = DashboardUsersListView.as_view()


class DashboardUsersDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Dashboard users detail view.

    Description: This view is used to display the details of a user.

    Attributes:
        model (User): The model used to display the details of a user.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.

    """

    model = User
    template_name = "dashboard/views/users/dashboard_users_detail.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        return context


dashboard_users_detail_view = DashboardUsersDetailView.as_view()


class DashboardUsersUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Dashboard users update view.

    Description: This view is used to update a user.

    Attributes:
        model (User): The model used to update a user.
        template_name (str): The template used to render the view.
        form_class (UserUpdateForm): The form used to update a user.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.
        test_func (Any): Returns the test function to be used in the view.
        get_initial (Any): Returns the initial data to be used in the form.
        form_valid (Any): Updates the user.

    """

    model = User
    template_name = "dashboard/views/users/dashboard_users_update.html"
    form_class = UserUpdateForm

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        return reverse("dashboard:user-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard
        return context

    def get_initial(self):
        return {
            "user": self.object,
        }

    def form_valid(self, form):
        new_log = DashboardAction(
            action_type="update",
            dash_board=self.request.user.dashboard,
            description=f"User {self.object.username} updated",
        )
        new_log.save()
        return super().form_valid(form)


dashboard_users_update_view = DashboardUsersUpdateView.as_view()


class DashboardUsersDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Dashboard users delete view.

    Description: This view is used to delete a user.

    Attributes:
        model (User): The model used to delete a user.
        template_name (str): The template used to render the view.
        form_class (UserDeleteForm): The form used to delete a user.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_success_url (str): Returns the URL to redirect to after the user is deleted.
        get_initial (Any): Returns the initial data to be used in the form.
        get_form_kwargs (Any): Returns the form kwargs to be used in the form.

    """

    model = User
    template_name = "dashboard/views/users/dashboard_users_delete.html"

    def get_success_url(self):
        return reverse("dashboard:user-list")

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """Get the context data.

        Description: This method is used to get the context data.
            It calls the superclass method to get the context data.
            It adds the user to the context data.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: The context data.

        """

        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.request.user.dashboard

        return context

    def delete(self, request, *args, **kwargs):
        """Delete the user.

        Description: This method is used to delete the user.
            It calls the superclass method to delete the user.
            It creates a new log for the user.

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
            description=f"User {self.object.username} deleted",
        )
        new_log.save()
        self.object = self.get_object()
        success_url = self.get_success_url()
        user: User = self.object
        if user.is_active:
            user.is_active = False
            user.save()
        return HttpResponseRedirect(success_url)


dashboard_users_delete_view = DashboardUsersDeleteView.as_view()
