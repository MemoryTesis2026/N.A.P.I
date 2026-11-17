import pathlib

from django.conf import settings
from django.core.files import File
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.http.response import FileResponse
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView

from lideresas.apps.documents.tasks import bytes_to_file
from lideresas.apps.documents.tasks import recursive_mkdir


class DetailedFileDownloadView(DetailView):
    """Detailed file download view.

    Description: This view is used to download a file.
        It is used to download a file from a DetailView.
        The file is downloaded as an attachment with the original filename.
        The file is also downloaded with a X-Accel-Redirect header to cache the file.

    Attributes:
        model (File): The model used to download the file.
        template_name (str): The template used to render the view.

    Methods:
        get_object (Any): Returns the object to be downloaded.
        get_success_url (str): Returns the URL to redirect to after the file is downloaded.
    """

    def get(self, request, *args, **kwargs):
        """Get the file to be downloaded.

        Description: This method is used to get the file to be downloaded.
            It checks if the user is authenticated and if the file exists.
            If the file exists, it returns a FileResponse with the file as an attachment.
            If the file does not exist, it returns a 404 Not Found response.

        Args:
            request (HttpRequest): The request object.
            *args (Any): Additional arguments.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            HttpResponse: The response to be returned.

        Raises:
            Http404: If the file does not exist.

        """

        obj = self.get_object()
        response: FileResponse = FileResponse(
            as_attachment=True,
            filename=obj.file,
        )
        response["Content-Disposition"] = "attachment; filename=" + obj.file
        response["X-Accel-Redirect"] = obj.file
        return response


class FileToPathCreateView(CreateView):
    """File to path create view.

    Description: This view is used to create a new file.
        It is used to create a new file in a specified path.
        The file is uploaded to the specified path.

    Attributes:
        model (File): The model used to create the file.
        form_class (ModelForm): The form used to create the file.
        template_name (str): The template used to render the view.

    Methods:
        get_object (Any): Returns the object to be created.
        get_success_url (str): Returns the URL to redirect to after the file is created.
        form_valid (Any): Creates the file.
    """

    model = File
    form_class = ModelForm
    template_name = "documents/views/file_to_path_create.html"

    def get_object(self, queryset: any):
        return super().get_object(queryset)

    paths: list[str] = None
    file_prefix: str = None
    object = None

    def get_paths(self) -> list[str]:
        """Get the paths.

        Description: This method is used to get the paths.
            It checks if the user is authenticated and if the paths are set.
            If the paths are set, it returns the paths.
            If the paths are not set, it raises an AttributeError.

        Returns:
            list[str]: The paths.

        Raises:
            AttributeError: If the paths are not set.

        """

        if self.paths is None:
            msg = "FileToPathView need a paths list of str that can be the paths"
            raise AttributeError(msg)
        return self.paths

    def get_file_prefix(self) -> str:
        """Get the file prefix.

        Description: This method is used to get the file prefix.
            It checks if the user is authenticated and if the file prefix is set.
            If the file prefix is set, it returns the file prefix.
            If the file prefix is not set, it raises an AttributeError.

        Returns:
            str: The file prefix.

        Raises:
            AttributeError: If the file prefix is not set.

        """

        if self.file_prefix is None:
            msg = "FileToPathView need a file_prefix to append to the file name"
            raise AttributeError(msg)
        return self.file_prefix

    def form_valid(self, form: ModelForm):
        """Create the file.

        Description: This method is used to create the file.
            It checks if the user is authenticated and if the file is valid.
            If the file is valid, it creates the file and redirects to the success URL.
            If the file is not valid, it returns a 400 Bad Request response.

        Args:
            form (ModelForm): The form used to create the file.

        Returns:
            HttpResponse: The response to be returned.

        Raises:
            Http400: If the file is not valid.

        """

        data = form.cleaned_data
        data.pop("file")
        self.object = self.model(**data)
        self.object.save()

        # buffering
        file = File(form.files["file"])
        path = recursive_mkdir(
            base_path=pathlib.Path(settings.PROTECTED_ROOT),
            joins=self.get_paths(),
        )
        file_path = bytes_to_file(
            path=path / f"{self.get_file_prefix()}-{file.name}",
            file=file,
        )
        if file_path is None:
            self.object.delete()
            return super().form_invalid(form)
        self.object.file = (
            "/".join(self.get_paths()) + self.get_file_prefix() + file.name
        )
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
