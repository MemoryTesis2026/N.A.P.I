from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BalancesConfig(AppConfig):
    """BalancesConfig class.
    The balance app is for managing balances. It provides models for balances,
    balance transactions,and balance transactions.

    """

    name = "lideresas.apps.balances"
    verbose_name = _("Balances")
