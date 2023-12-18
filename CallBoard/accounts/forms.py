from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from accounts.models import OneTimeCode


class BaseSignupForm(UserCreationForm):

    class Meta:

        model = User
        fields = [
            'username',
            'email',
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if email is None or email == "":
            raise ValidationError({
                "email": "This field is required."
            })

        return cleaned_data


class OneTimeCodeForm(ModelForm):

    class Meta:

        model = OneTimeCode
        fields = ('code',)
