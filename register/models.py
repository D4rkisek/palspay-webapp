from django.conf import settings
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    # Add currency field if supporting multiple currencies
    currency = models.CharField(max_length=3, choices=[('GBP', 'Pounds'), ('USD', 'Dollars'), ('EUR', 'Euros')],
                                default='GBP')


# New Staff model
class Staff(models.Model):
    user_admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff')
#    def __str__(self):
#        return f"{self.user.username} - {self.department}"


# Early stage of the transaction model
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)  # e.g., "deposit", "withdrawal", "payment"
    description = models.TextField()

    def __str__(self):
        return f"Transaction {self.id} on {self.account}"


# Money requests
class MoneyRequest(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_requests')
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_accepted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_responded = models.DateTimeField(null=True, blank=True)
