from django.urls import path

from .views import dashboard_audit_detail_view
from .views import dashboard_audit_list_view
from .views import dashboard_detail_view
from .views import dashboard_organization_delete_view
from .views import dashboard_organization_detail_view
from .views import dashboard_organization_list_view
from .views import dashboard_organization_update_view
from .views import dashboard_project_delete_view
from .views import dashboard_project_detail_view
from .views import dashboard_project_list_view
from .views import dashboard_project_update_view
from .views import dashboard_users_delete_view
from .views import dashboard_users_detail_view
from .views import dashboard_users_list_view
from .views import dashboard_users_update_view

app_name = "dashboard"
urlpatterns = [
    path("", view=dashboard_detail_view, name="index"),
    path(
        "organizations/",
        view=dashboard_organization_list_view,
        name="organization-list",
    ),
    path(
        "organizations/create/",
        view=dashboard_organization_detail_view,
        name="organization-create",
    ),
    path(
        "organizations/update/<int:pk>",
        view=dashboard_organization_update_view,
        name="organization-update",
    ),
    path(
        "organizations/delete/<int:pk>",
        view=dashboard_organization_delete_view,
        name="organization-delete",
    ),
    path(
        "organizations/<str:pk>/",
        view=dashboard_organization_detail_view,
        name="organization-detail",
    ),
    path(
        "projects/",
        view=dashboard_project_list_view,
        name="project-list",
    ),
    path(
        "projects/create/",
        view=dashboard_project_detail_view,
        name="project-create",
    ),
    path(
        "projects/update/<int:pk>",
        view=dashboard_project_update_view,
        name="project-update",
    ),
    path(
        "projects/delete/<int:pk>",
        view=dashboard_project_delete_view,
        name="project-delete",
    ),
    path(
        "projects/<str:pk>/",
        view=dashboard_project_detail_view,
        name="project-detail",
    ),
    path(
        "audit/",
        view=dashboard_audit_list_view,
        name="audit-list",
    ),
    path(
        "audit/<int:pk>/",
        view=dashboard_audit_detail_view,
        name="audit-detail",
    ),
    path(
        "users/",
        view=dashboard_users_list_view,
        name="user-list",
    ),
    path(
        "users/update/<int:pk>",
        view=dashboard_users_update_view,
        name="user-update",
    ),
    path(
        "users/delete/<int:pk>",
        view=dashboard_users_delete_view,
        name="user-delete",
    ),
    path(
        "users/<str:pk>/",
        view=dashboard_users_detail_view,
        name="user-detail",
    ),
]
