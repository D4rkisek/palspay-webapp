from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class TransferMoneyForm(forms.Form):
    username = forms.CharField(max_length=150, label='Recipient Username')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Amount')