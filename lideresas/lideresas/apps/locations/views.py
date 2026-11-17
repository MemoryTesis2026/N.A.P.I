from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import TemplateView

from .models import Comuna
from .models import Location
from .models import Province
from .models import Region


class RegionListView(ListView, LoginRequiredMixin):
    """Region list view.
        htmx: true

    Description: This view is used to list the regions.
        It is used to list the regions.
        is a component of the location selector.

    Attributes:
        model (Region): The model used to list the regions.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = Region
    template_name = "locations/components/region_selector.html"

    def get_queryset(self):
        return super().get_queryset().order_by("-number")


region_list_view = RegionListView.as_view()


class ProvinceListView(ListView, LoginRequiredMixin):
    """Province list view.

    Description: This view is used to list the provinces.
        It is used to list the provinces.
        is a component of the location selector.

    Attributes:
        model (Province): The model used to list the provinces.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = Province
    template_name = "locations/components/province_selector.html"

    def get_queryset(self):
        """Get the queryset.

        Description: This method is used to get the queryset.
            It filters the queryset to include only the provinces that belong to the region.

        Returns:
            QuerySet: The queryset.

        """

        queryset = super().get_queryset()
        if "region" in self.request.GET:
            return queryset.filter(region__pk=self.request.GET["region"]).order_by(
                "-name",
            )
        return queryset.order_by("-name")


provicen_list_view = ProvinceListView.as_view()


class ComunaListView(ListView, LoginRequiredMixin):
    """Comuna list view.

    Description: This view is used to list the comunas.
        It is used to list the comunas.
        is a component of the location selector.

    Attributes:
        model (Comuna): The model used to list the comunas.
        template_name (str): The template used to render the view.

    Methods:
        get_queryset (Any): Returns the queryset to be used in the view.

    """

    model = Comuna
    template_name = "locations/components/comuna_selector.html"

    def get_queryset(self):
        """Get the queryset.

        Description: This method is used to get the queryset.
            It filters the queryset to include only the comunas that belong to the province.

        Returns:
            QuerySet: The queryset.

        """

        queryset = super().get_queryset()
        if "province" in self.request.GET:
            return queryset.filter(province__pk=self.request.GET["province"]).order_by(
                "-name",
            )
        return queryset.order_by("-name")


comuna_list_view = ComunaListView.as_view()


class LocationCreateView(TemplateView, LoginRequiredMixin):
    """Location create view.

    Description: This view is used to create a new location.
        It is used to create a new location.
        is a component of the location selector.

    Attributes:
        model (Location): The model used to create a new location.
        template_name (str): The template used to render the view.

    Methods:
        get_context_data (Any): Returns the context data to be used in the template.

    """

    model = Location
    template_name = "locations/views/location_create.html"

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


location_create_view = LocationCreateView.as_view()
