from django.urls import path

from .views import organization_create_view
from .views import organization_delete_view
from .views import organization_detail_view
from .views import organization_list_view
from .views import organization_set_location_view
from .views import organization_update_view

app_name = "organizations"
urlpatterns = [
    path("", view=organization_list_view, name="organization-list"),
    path("create/", view=organization_create_view, name="organization-create"),
    path("delete/<int:pk>", view=organization_delete_view, name="organization-delete"),
    path("update/<int:pk>", view=organization_update_view, name="organization-update"),
    path(
        "location/<int:pk>",
        view=organization_set_location_view,
        name="organization-set-location",
    ),
    path("<str:pk>/", view=organization_detail_view, name="organization-detail"),
]
