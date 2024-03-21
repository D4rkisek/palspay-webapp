from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MemberCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    fname = forms.CharField(required=True, max_length=50)
    lname = forms.CharField(required=True, max_length=50)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('fname', 'lname', 'email',)
