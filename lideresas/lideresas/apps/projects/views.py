from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from lideresas.apps.documents.mixins import DetailedFileDownloadView
from lideresas.apps.locations.models import Location
from lideresas.apps.locations.models import Region

from .forms import ProjectCreateForm
from .forms import ProjectDocumentCreateForm
from .forms import ProjectDocumentUpdateForm
from .forms import ProjectSetLocationForm
from .forms import ProjectTransactionCreateForm
from .forms import ProjectTransactionUpdateForm
from .forms import ProjectUpdateForm
from .models import Project
from .models import ProjectDocument
from .models import ProjectTransaction

if TYPE_CHECKING:
    from django.http import QueryDict


class ProjectDetailView(DetailView, LoginRequiredMixin):
    """Project detail view.

    Description: This view is used to display the details of a project.

    Attributes:
        model (Project): The model used to display the details of a project.
        template_name (str): The template used to render the view.
        slug_field (str): The field used to generate the URL for the project.
        slug_url_kwarg (str): The URL argument used to generate the URL for the project.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = Project
    template_name = "project/views/project_detail.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


project_detail_view = ProjectDetailView.as_view()


class ProjectListView(ListView, LoginRequiredMixin):
    """Project list view.

    Description: This view is used to list the projects of a user.

    Attributes:
        model (Project): The model used to list the projects of a user.
        template_name (str): The template used to render the view.
        paginate_by (int): The number of items to be displayed per page.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_context_data (Any): Returns the context data to be used in the template.


    """

    model = Project
    template_name = "project/views/project_list.html"

    def get_queryset(self):
        """Get the queryset.

        Description: This method is used to get the queryset.
            It filters the queryset to include only the projects that belong to the user.

        Returns:
            QuerySet: The queryset.
        """

        queryset = super().get_queryset().filter(owner=self.request.user)

        if "organization" in self.request.GET:
            return queryset.filter(organization__pk=self.request.GET["organization"])
        return queryset


project_list_view = ProjectListView.as_view()


class ProjectCreateView(CreateView, LoginRequiredMixin):
    """Project create view.

    Description: This view is used to create a new project.

    Attributes:
        model (Project): The model used to create a new project.
        template_name (str): The template used to render the view.
        form_class (ProjectCreateForm): The form used to create a new project.

    Methods:
        get_success_url (str): Returns the URL to redirect to after the project is created.
        get_initial (Any): Returns the initial data to be used in the form.
        get_form_kwargs (Any): Returns the form kwargs to be used in the form.

    """

    model = Project
    template_name = "project/views/project_create.html"
    form_class = ProjectCreateForm

    def get_success_url(self):
        return reverse(
            "projects:project-set-location",
            kwargs={"pk": self.object.pk},
        )

    def get_initial(self) -> dict[str, Any]:
        return {"owner": self.request.user.pk}

    def get_form_kwargs(self) -> dict[str, Any]:
        """Get the form kwargs.

        Description: This method is used to get the form kwargs.
            It calls the superclass method to get the form kwargs.
            It adds the user to the form kwargs.

        Returns:
            dict[str, Any]: The form kwargs.

        """

        data = super().get_form_kwargs()
        data["user"] = self.request.user
        return data


project_create_view = ProjectCreateView.as_view()


class ProjectSetLocationView(FormView, LoginRequiredMixin):
    """Project set location view.

    Description: This view is used to set the location of a project.

    Attributes:
        model (Project): The model used to set the location of a project.
        template_name (str): The template used to render the view.
        form_class (ProjectSetLocationForm): The form used to set the location of a project.

    Methods:
        get_success_url (str): Returns the URL to redirect to after the location is set.
        get_context_data (Any): Returns the context data to be used in the template.
        get_initial (Any): Returns the initial data to be used in the form.
        form_valid (Any): Sets the location of the project.

    """

    model = Project
    template_name = "project/views/project_set_location.html"
    form_class = ProjectSetLocationForm

    def get_success_url(self):
        return reverse(
            "projects:project-detail",
            kwargs={"pk": self.kwargs["pk"]},
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get the context data.

        Description: This method is used to get the context data.
            It calls the superclass method to get the context data.
            It adds the regions and the project to the context data.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: The context data.

        """

        context = super().get_context_data(**kwargs)
        context["regions"] = Region.objects.all()
        context["project"] = (
            get_object_or_404(
                Project,
                pk=self.kwargs["pk"],
                owner=self.request.user,
            ),
        )
        return context

    def get_initial(self):
        return {
            "project": get_object_or_404(
                Project,
                pk=self.kwargs["pk"],
                owner=self.request.user,
            ),
        }

    def form_valid(self, form: ProjectSetLocationForm):
        """Set the location of the project.

        Description: This method is used to set the location of the project.
            It creates a new location object and saves it to the project.
            It then saves the project.

        Args:
            form (ProjectSetLocationForm): The form used to set the location of the project.

        Returns:
            HttpResponse: The response to be returned.

        """

        new_location = Location(
            comuna=form.cleaned_data["comuna"],
            street=form.cleaned_data["street"],
            number=form.cleaned_data["number"],
        )
        project: Project = get_object_or_404(
            Project,
            pk=self.kwargs["pk"],
            owner=self.request.user,
        )
        project.location = new_location
        new_location.save()
        project.save()
        return super().form_valid(form)


project_set_location_view = ProjectSetLocationView.as_view()


class ProjectUpdateView(UpdateView, LoginRequiredMixin):
    """Project update view.

    Description: This view is used to update a project.

    Attributes:
        model (Project): The model used to update a project.
        template_name (str): The template used to render the view.
        form_class (ProjectUpdateForm): The form used to update a project.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = Project
    template_name = "project/views/project_update.html"
    form_class = ProjectUpdateForm

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


project_update_view = ProjectUpdateView.as_view()


class ProjectDeleteView(DeleteView, LoginRequiredMixin):
    """Project delete view.

    Description: This view is used to delete a project.

    Attributes:
        model (Project): The model used to delete a project.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_success_url (str): Returns the URL to redirect to after the project is deleted.

    """

    model = Project
    template_name = "project/views/project_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_success_url(self):
        return reverse("projects:project-list")


project_delete_view = ProjectDeleteView.as_view()


class ProjectDocumentDetailView(DetailedFileDownloadView, LoginRequiredMixin):
    """Project document detail view.

    Description: This view is used to download a document of a project.

    Attributes:
        model (ProjectDocument): The model used to download the document of a project.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = ProjectDocument
    template_name = "project/views/project_document_detail.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"


projectdocument_detail_view = ProjectDocumentDetailView.as_view()


class ProjectDocumentListView(ListView, LoginRequiredMixin):
    """Project document list view.

    Description: This view is used to list the documents of a project.

    Attributes:
        model (ProjectDocument): The model used to list the documents of a project.
        template_name (str): The template used to render the view.

    Methods:
        get_context_data (Any): Returns the context data to be used in the template.
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = ProjectDocument
    template_name = "project/views/project_document_list.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["project"] = get_object_or_404(Project, pk=self.kwargs["project"])
        return data

    def get_queryset(self):
        """Get the queryset.

        Description: This method is used to get the queryset.
            It filters the queryset to include only the documents that belong to the project.

        Returns:
            QuerySet: The queryset.
        """

        return (
            super()
            .get_queryset()
            .filter(project__owner=self.request.user)
            .filter(~Q(document_type="boleta"))
            .filter(project=self.kwargs["project"])
        )


projectdocument_list_view = ProjectDocumentListView.as_view()


class ProjectDocumentCreateView(CreateView, LoginRequiredMixin):
    """Project document create view.

    Description: This view is used to create a new document for a project.

    Attributes:
        model (ProjectDocument): The model used to create a new document for a project.
        template_name (str): The template used to render the view.
        form_class (ProjectDocumentCreateForm): The form used to create a new document for a project.

    Methods:
        get_success_url (str): Returns the URL to redirect to after the document is created.
        get_initial (Any): Returns the initial data to be used in the form.
        get_form_kwargs (Any): Returns the form kwargs to be used in the form.
        get_file_prefix (Any): Returns the file prefix to be used in the form.
        get_paths (Any): Returns the paths to be used in the form.

    """

    model = ProjectDocument
    template_name = "project/views/project_document_create.html"
    form_class = ProjectDocumentCreateForm

    def get_success_url(self):
        return reverse(
            "projects:document-list",
            kwargs={"project": self.object.project.pk},
        )

    def get_initial(self):
        """Get the initial data.

        Description: This method is used to get the initial data.
            It calls the superclass method to get the initial data.
            It adds the project to the initial data if it is not in the GET parameters.

        Returns:
            dict[str, Any]: The initial data.

        """

        initial = super().get_initial()
        if "project" not in self.request.GET:
            return initial
        initial["project"] = get_object_or_404(
            Project,
            pk=self.request.GET["project"],
        )
        return initial

    def get_form_kwargs(self) -> dict[str, Any]:
        """Get the form kwargs.

        Description: This method is used to get the form kwargs.
            It calls the superclass method to get the form kwargs.
            It adds the user to the form kwargs.
            It adds the project to the form kwargs if the request method is POST or PUT.

        Variables:
            data (dict[str, Any]): The form kwargs.
            file (File): The file to be added to the form kwargs.
            file_name (str): The name of the file. It is used to generate the file name.

        Returns:
            dict[str, Any]: The form kwargs.

        Raises:
            Http404: If the project is not found.

        """

        data = dict(super().get_form_kwargs())
        data["user"] = self.request.user
        if self.request.method in ("POST", "PUT"):
            file = data["files"]["file"]
            file.name = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}:{self.request.user.pk}+{data['initial']['project'].pk}-{file.name}"
        return data


projectdocument_create_view = ProjectDocumentCreateView.as_view()


class ProjectDocumentUpdateView(UpdateView, LoginRequiredMixin):
    """Project document update view.

    Description: This view is used to update a document of a project.

    Attributes:
        model (ProjectDocument): The model used to update a document of a project.
        template_name (str): The template used to render the view.
        form_class (ProjectDocumentUpdateForm): The form used to update a document of a project.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = ProjectDocument
    template_name = "project/views/project_document_update.html"
    form_class = ProjectDocumentUpdateForm

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)


projectdocument_update_view = ProjectDocumentUpdateView.as_view()


class ProjectDocumentDeleteView(DeleteView, LoginRequiredMixin):
    """Project document delete view.

    Description: This view is used to delete a document of a project.

    Attributes:
        model (ProjectDocument): The model used to delete a document of a project.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_success_url (str): Returns the URL to redirect to after the document is deleted.

    """

    model = ProjectDocument
    template_name = "project/views/project_document_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse(
            "projects:document-list",
            kwargs={"project": self.object.project.pk},
        )


projectdocument_delete_view = ProjectDocumentDeleteView.as_view()


class ProjectTransactionDetailView(DetailedFileDownloadView, LoginRequiredMixin):
    """Project transaction detail view.

    Description: This view is used to download a transaction of a project.

    Attributes:
        model (ProjectTransaction): The model used to download the transaction of a project.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = ProjectTransaction
    template_name = "projects/views/project_boleta_detail.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)


project_transaction_detail_view = ProjectTransactionDetailView.as_view()


class ProjectTransactionListView(ListView, LoginRequiredMixin):
    """Project transaction list view.

    Description: This view is used to list the transactions of a project.

    Attributes:
        model (ProjectTransaction): The model used to list the transactions of a project.
        template_name (str): The template used to render the view.

    Methods:
        get_context_data (Any): Returns the context data to be used in the template.
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = ProjectTransaction
    template_name = "project/views/transactions/project_transaction_list.html"

    def get_context_data(self, **kwargs):
        """Get the context data.

        Description: This method is used to get the context data.
            It calls the superclass method to get the context data.
            It adds the project to the context data if it is in the GET parameters.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: The context data.

        Raises:
            Http404: If the project is not found.
        """

        data = super().get_context_data(**kwargs)
        data["project"] = get_object_or_404(Project, pk=self.kwargs["project"])
        return data

    def get_queryset(self):
        """Get the queryset.

        Description: This method is used to get the queryset.
            It filters the queryset to include only the transactions that belong to the project.

        Returns:
            QuerySet: The queryset.

        Raises:
            Http404: If the project is not found.
        """

        queryset = super().get_queryset().filter(project__owner=self.request.user)
        if "project" in self.request.GET:
            return queryset.filter(project__pk=self.request.GET["project"])
        return queryset


project_transaction_list_view = ProjectTransactionListView.as_view()


class ProjectTransactionCreateView(CreateView, LoginRequiredMixin):
    """Project transaction create view.

    Description: This view is used to create a new transaction for a project.

    Attributes:
        model (ProjectTransaction): The model used to create a new transaction for a project.
        template_name (str): The template used to render the view.
        form_class (ProjectTransactionCreateForm): The form used to create a new transaction for a project.

    Methods:
        get_success_url (str): Returns the URL to redirect to after the transaction is created.
        get_initial (Any): Returns the initial data to be used in the form.
        get_form_kwargs (Any): Returns the form kwargs to be used in the form.
        get_file_prefix (Any): Returns the file prefix to be used in the form.
        get_paths (Any): Returns the paths to be used in the form.

    """

    model = ProjectTransaction
    template_name = "project/views/transactions/project_transaction_create.html"
    form_class = ProjectTransactionCreateForm

    def get_success_url(self):
        return reverse(
            "projects:document-list",
            kwargs={"project": self.object.project.pk},
        )

    def get_initial(self):
        """Get the initial data.

        Description: This method is used to get the initial data.
            It calls the superclass method to get the initial data.
            It adds the project to the initial data if it is not in the GET parameters.

        Returns:
            dict[str, Any]: The initial data.

        Raises:
            Http404: If the project is not found.
        """

        initial = super().get_initial()
        if "project" not in self.request.GET:
            return initial
        initial["project"] = get_object_or_404(
            Project,
            pk=self.request.GET["project"],
        )
        return initial

    def get_form_kwargs(self) -> dict[str, Any]:
        """Get the form kwargs.

        Description: This method is used to get the form kwargs.
            It calls the superclass method to get the form kwargs.
            It adds the user to the form kwargs.
            It adds the project to the form kwargs if the request method is POST or PUT.

        Returns:
            dict[str, Any]: The form kwargs.

        Raises:
            Http404: If the project is not found.
        """

        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        if self.request.method in ("POST", "PUT"):
            data: QueryDict = kwargs["data"].copy()
            data["balance"] = get_object_or_404(Project, pk=data["project"])
            kwargs["data"] = data
            file = data["files"]["file"]
            file.name = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}:{self.request.user.pk}+{data['initial']['project'].pk}-{file.name}"
        return kwargs

    def form_valid(self, form):
        form.cleaned_data["balance"] = form.cleaned_data["project"]
        return super().form_valid(form)


project_transaction_create_view = ProjectTransactionCreateView.as_view()


class ProjectTransactionUpdateView(UpdateView, LoginRequiredMixin):
    """Project transaction update view.

    Description: This view is used to update a transaction of a project.

    Attributes:
        model (ProjectTransaction): The model used to update a transaction of a project.
        template_name (str): The template used to render the view.
        form_class (ProjectTransactionUpdateForm): The form used to update a transaction of a project.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = ProjectTransaction
    template_name = "project/views/transactions/project_transaction_update.html"
    form_class = ProjectTransactionUpdateForm

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)


project_transaction_update_view = ProjectTransactionUpdateView.as_view()


class ProjectTransactionDeleteView(DeleteView, LoginRequiredMixin):
    """Project transaction delete view.

    Description: This view is used to delete a transaction of a project.

    Attributes:
        model (ProjectTransaction): The model used to delete a transaction of a project.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.
        get_success_url (str): Returns the URL to redirect to after the transaction is deleted.

    """

    model = ProjectTransaction
    template_name = "project/views/transactions/project_transaction_delete.html"

    def get_queryset(self):
        """Get the queryset.

        Description: This method is used to get the queryset.
            It filters the queryset to include only the transactions that belong to the project.

        Returns:
            QuerySet: The queryset.

        Raises:
            Http404: If the project is not found.

        """
        return super().get_queryset().filter(project__owner=self.request.user)

    def get_success_url(self):
        return super().get_success_url()


project_transaction_delete_view = ProjectTransactionDeleteView.as_view()
