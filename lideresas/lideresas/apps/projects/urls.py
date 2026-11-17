from django.urls import path

from .views import project_create_view
from .views import project_delete_view
from .views import project_detail_view
from .views import project_list_view
from .views import project_set_location_view
from .views import project_transaction_create_view
from .views import project_transaction_detail_view
from .views import project_transaction_list_view
from .views import project_update_view
from .views import projectdocument_create_view
from .views import projectdocument_delete_view
from .views import projectdocument_detail_view
from .views import projectdocument_list_view

app_name = "projects"
urlpatterns = [
    path("", view=project_list_view, name="project-list"),
    path("create/", view=project_create_view, name="project-create"),
    path("delete/<str:pk>", view=project_delete_view, name="project-delete"),
    path("update/<str:pk>", view=project_update_view, name="project-update"),
    path(
        "location/<str:pk>",
        view=project_set_location_view,
        name="project-set-location",
    ),
    path(
        "documents/list/<int:project>",
        view=projectdocument_list_view,
        name="document-list",
    ),
    path(
        "documents/create/",
        view=projectdocument_create_view,
        name="document-create",
    ),
    path(
        "documents/<int:pk>/",
        view=projectdocument_detail_view,
        name="document-detail",
    ),
    path(
        "documents/delete/<int:pk>/",
        view=projectdocument_delete_view,
        name="document-delete",
    ),
    path(
        "transaction/list/<int:project>",
        view=project_transaction_list_view,
        name="transaction-list",
    ),
    path(
        "transaction/create/",
        view=project_transaction_create_view,
        name="transaction-create",
    ),
    path(
        "transaction/<int:pk>/",
        view=project_transaction_detail_view,
        name="transaction-detail",
    ),
    path("<str:pk>/", view=project_detail_view, name="project-detail"),
]
