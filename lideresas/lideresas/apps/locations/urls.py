from django.urls import URLPattern
from django.urls import path

from .views import comuna_list_view
from .views import location_create_view
from .views import provicen_list_view
from .views import region_list_view

app_name = "locations"
urlpatterns: list[URLPattern] = [
    path("regions/", view=region_list_view, name="region-list"),
    path("provinces/", view=provicen_list_view, name="provinces-list"),
    path("comunas/", view=comuna_list_view, name="comunas-list"),
    path("location/create/", view=location_create_view, name="location-create"),
]
