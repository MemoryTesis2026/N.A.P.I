from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class Balance(models.Model):
    """Balance model.

    Description: This model represents a balance.

    Attributes:
        name (CharField): The name of the balance.
        description (TextField): The description of the balance.
        initial_balance (BigIntegerField): The initial balance of the balance.

    Methods:
        __str__ (str): Returns the string representation of the balance.
        get_absolute_url (str): Returns the URL for the balance.
        get_all_transactions (QuerySet): Returns all the transactions of the balance.
        get_all_positive_transactions (QuerySet): Returns all the positive transactions of the balance.
        get_all_negative_transactions (QuerySet): Returns all the negative transactions of the balance.
        get_actual_balance (int): Returns the actual balance of the balance.

    Example:
        >>> from lideresas.balances.models import Balance
        >>> balance = Balance.objects.create(initial_balance=100)
        >>> balance.initial_balance
        100
        >>> balance.get_actual_balance()
        100
        >>> balance.get_all_transactions()
        <QuerySet [<BalanceTransaction: Test Transaction>]>
        >>> balance.get_all_positive_transactions()
        <QuerySet [<BalanceTransaction: Test Transaction>]>
        >>> balance.get_all_negative_transactions()
        <QuerySet []>
        >>> balance.get_absolute_url()
        '/balances/1/'

    """

    initial_balance = models.BigIntegerField(_("Initial Balance"), default=0)

    class Meta:
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")
        abstract = True

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("balances:balance-detail", kwargs={"pk": self.pk})

    def get_all_transactions(self) -> models.QuerySet:
        return self.transactions.all()

    def get_all_positive_transactions(self) -> models.QuerySet:
        return self.get_all_transactions().filter(transaction_type="+")

    def get_all_negative_transactions(self) -> models.QuerySet:
        return self.get_all_transactions().filter(transaction_type="-")

    @cached_property
    def get_actual_balance(self) -> int:
        """Get the actual balance of the balance.

        Description: This method is used to get the actual balance of the balance.
            It calculates the actual balance by adding the positive transactions and
            subtracting the negative transactions.

        Returns:
            int: The actual balance of the balance.
        """

        positive_amount = [x.amount for x in self.get_all_positive_transactions()]
        negative_amount = [x.amount for x in self.get_all_negative_transactions()]
        return self.initial_balance + sum(positive_amount) - sum(negative_amount)


class BalanceTransaction(models.Model):
    """BalanceTransaction model.

    Description: This model represents a transaction of a balance.

    Attributes:
        balance (ForeignKey): The balance of the transaction.
        transaction_type (CharField): The type of the transaction.
        amount (PositiveIntegerField): The amount of the transaction.

    Methods:
        __str__ (str): Returns the string representation of the transaction.
        get_absolute_url (str): Returns the URL for the transaction.

    Example:
        >>> from lideresas.project.models import ProjectTransaction
        >>> transaction = ProjectTransaction.objects.create(name="Test Transaction")
        >>> transaction.name
        'Test Transaction'

    """

    transaction_types = (("+", _("Positive")), ("-", _("Negative")))

    transaction_type = models.CharField(
        _("Transaction type"),
        choices=transaction_types,
        max_length=4,
    )

    amount = models.PositiveIntegerField(_("Transaction amount"), default=0)

    class Meta:
        verbose_name = _("Balance transaction")
        verbose_name_plural = _("Balance transactions")
        abstract = True

    def __str__(self):
        return f"{self.amount}-{self.transaction_type}"

    def get_absolute_url(self):
        return reverse("balances:balance-transaction-detail", kwargs={"pk": self.pk})
