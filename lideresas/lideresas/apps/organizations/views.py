from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from lideresas.apps.locations.models import Location
from lideresas.apps.locations.models import Region

from .forms import OrganizationCreateForm
from .forms import OrganizationSetLocationForm
from .forms import OrganizationUpdateForm
from .models import Organization


class OrganizationDetailView(DetailView, LoginRequiredMixin):
    """Organization detail view.

    Description: This view is used to display the details of an organization.

    Attributes:
        model (Organization): The model used to display the details of an organization.
        template_name (str): The template used to render the view.
        slug_field (str): The field used to generate the URL for the organization.
        slug_url_kwarg (str): The URL argument used to generate the URL for the organization.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = Organization
    template_name = "organization/views/organization_detail.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


organization_detail_view = OrganizationDetailView.as_view()


class OrganizationListView(ListView, LoginRequiredMixin):
    """Organization list view.

    Description: This view is used to list the organizations of a user.

    Attributes:
        model (Organization): The model used to list the organizations of a user.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = Organization
    template_name = "organization/views/organization_list.html"

    def get_queryset(self):
        """Get the queryset.

        Description: This method is used to get the queryset.
        It filters the queryset to include only the organizations that belong to the user.

        Returns:
            QuerySet: The queryset.
        """

        return super().get_queryset().filter(owner=self.request.user)


organization_list_view = OrganizationListView.as_view()


class OrganizationCreateView(CreateView, LoginRequiredMixin):
    """Organization create view.

    Description: This view is used to create a new organization.

    Attributes:
        model (Organization): The model used to create a new organization.
        template_name (str): The template used to render the view.
        form_class (OrganizationCreateForm): The form used to create a new organization.
        queryset (Organization): The queryset used to create a new organization.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_success_url (str): Returns the URL to redirect to after the organization is created.
        get_initial (Any): Returns the initial data to be used in the form.
        get_form_kwargs (Any): Returns the form kwargs to be used in the form.

    """

    model = Organization
    template_name = "organization/views/organization_create.html"
    form_class = OrganizationCreateForm
    queryset = Organization.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_success_url(self):
        return reverse(
            "organizations:organization-set-location",
            kwargs={"pk": self.object.pk},
        )

    def get_initial(self) -> dict[str, Any]:
        return {"owner": self.request.user.pk}

    def get_form_kwargs(self) -> dict[str, Any]:
        """Get the form kwargs.

        Description: This method is used to get the form kwargs.
            It adds the user to the form kwargs.

        Returns:
            dict[str, Any]: The form kwargs.

        """

        data = super().get_form_kwargs()
        data["user"] = self.request.user
        return data


organization_create_view = OrganizationCreateView.as_view()


class OrganizationUpdateView(UpdateView, LoginRequiredMixin):
    """Organization update view.

    Description: This view is used to update an organization.

    Attributes:
        model (Organization): The model used to update an organization.
        template_name (str): The template used to render the view.
        form_class (OrganizationUpdateForm): The form used to update an organization.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = Organization
    template_name = "organization/views/organization_update.html"
    form_class = OrganizationUpdateForm

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


organization_update_view = OrganizationUpdateView.as_view()


class OrganizationDeleteView(DeleteView, LoginRequiredMixin):
    """Organization delete view.

    Description: This view is used to delete an organization.

    Attributes:
        model (Organization): The model used to delete an organization.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_success_url (str): Returns the URL to redirect to after the organization is deleted.

    """

    model = Organization
    template_name = "organization/views/organization_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_success_url(self):
        return reverse("organizations:organization-list")


organization_delete_view = OrganizationDeleteView.as_view()


class OrganizationSetLocationView(FormView, LoginRequiredMixin):
    """Organization set location view.

    Description: This view is used to set the location of an organization.

    Attributes:
        model (Organization): The model used to set the location of an organization.
        template_name (str): The template used to render the view.
        form_class (OrganizationSetLocationForm): The form used to set the location of an organization.

    Methods:
        get_success_url (str): Returns the URL to redirect to after the location is set.
        get_context_data (Any): Returns the context data to be used in the template.
        get_initial (Any): Returns the initial data to be used in the form.
        form_valid (Any): Sets the location of the organization.

    """

    model = Organization
    template_name = "organization/views/organization_set_location.html"
    form_class = OrganizationSetLocationForm

    def get_success_url(self):
        return reverse(
            "organizations:organization-detail",
            kwargs={"pk": self.kwargs["pk"]},
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get the context data.

        Description: This method is used to get the context data.
            It calls the superclass method to get the context data.
            It adds the regions to the context data.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: The context data.
        """

        context = super().get_context_data(**kwargs)
        context["regions"] = Region.objects.all()
        return context

    def get_initial(self):
        """Get the initial data.

        Description: This method is used to get the initial data.
            It calls the superclass method to get the initial data.
            It adds the organization to the initial data if it is not in the GET parameters.

        Returns:
            dict[str, Any]: The initial data.

        """

        return {
            "organization": get_object_or_404(
                Organization,
                pk=self.kwargs["pk"],
                owner=self.request.user,
            ),
        }

    def form_valid(self, form: OrganizationSetLocationForm):
        """Set the location of the organization.

        Description: This method is used to set the location of the organization.
            It creates a new location object and saves it to the organization.
            It then saves the organization.

        Args:
            form (OrganizationSetLocationForm): The form used to set the location of the organization.

        Returns:
            HttpResponse: The response to be returned.

        """

        new_location = Location(
            comuna=form.cleaned_data["comuna"],
            street=form.cleaned_data["street"],
            number=form.cleaned_data["number"],
        )
        organization = get_object_or_404(
            Organization,
            pk=self.kwargs["pk"],
            owner=self.request.user,
        )
        organization.location = new_location
        new_location.save()
        organization.save()
        return super().form_valid(form)


organization_set_location_view = OrganizationSetLocationView.as_view()
