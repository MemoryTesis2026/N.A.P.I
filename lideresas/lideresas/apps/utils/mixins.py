from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.cache import cache_page

CACHE_ERROR_MESSAGE = "Cache timeout exceeded"
CACHE_KEY_ERROR_MESSAGE = "Cache key not set"
CACHE_TIMEOUT_ERROR_MESSAGE = "Cache timeout not set"


class CacheQuerysetMixin:
    cache_timeout: int = 60
    cache_key: str = None

    def get_cache_prefix(self) -> str:
        if not hasattr(self, "cache_key") or self.cache_key is None:
            raise AttributeError(CACHE_ERROR_MESSAGE)
        raise NotImplementedError

    def get_cache_timeout(self):
        if not hasattr(self, "cache_timeout"):
            raise AttributeError(CACHE_TIMEOUT_ERROR_MESSAGE)
        return self.cache_timeout

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)


class CachePageMixin:
    """CachePageMixin class.

    Attributes:
        cache_timeout (int): The cache timeout in seconds.

    Example:
        >>> class MyView(CachePageMixin, View):
        ...     cache_timeout = 60

    Raises:
        AttributeError: If the cache_timeout attribute is not set.
    """

    cache_timeout = 60

    def get_cache_timeout(self):
        if not hasattr(self, "cache_timeout"):
            raise AttributeError(CACHE_ERROR_MESSAGE)
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(
            super(CachePageMixin, self).dispatch
        )(
            *args,
            **kwargs,
        )


class AdminRequiredMixin(UserPassesTestMixin):
    """AdminRequiredMixin class.

    Description: This mixin is used to check if the user is an admin.
        It is used to check if the user is an admin.
        If the user is not an admin, it returns a 403 Forbidden response.

    Example:
        >>> class MyView(AdminRequiredMixin, TemplateView):
        ...     template_name = "my_template.html"

    Raises:
        PermissionDenied: If the user is not an admin.

    """

    def test_func(self):
        if self.request.user is None:
            return False
        return self.request.user.is_staff or self.request.user.is_superuser
