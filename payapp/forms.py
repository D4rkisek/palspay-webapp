from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class TransferMoneyForm(forms.Form):
    username = forms.CharField(max_length=150, label='Recipient Username')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Amount')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("User does not exist.")
        return username