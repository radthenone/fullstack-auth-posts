from apps.users.models import Roles, User, UserBasic, UserPremium
from apps.users.utils import set_username
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserForm(UserChangeForm):
    password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
        required=False,
    )
    password2 = forms.CharField(
        label="Check password",
        widget=forms.PasswordInput,
        strip=False,
        required=False,
    )
    roles = forms.ModelMultipleChoiceField(
        queryset=Roles.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "roles",
            "friends",
            "password",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError(
                f"Passwords don't match {password} not {password2}"
            )

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        roles = self.cleaned_data.get("roles")
        if email:
            user.username = set_username(email)
        if password:
            user.set_password(password)
        user.save()
        user.roles.set(roles)
        roles_list = list(roles.values_list("name", flat=True))
        try:
            if "BASIC" in roles_list:
                UserBasic.objects.create(user=user)
            if "PREMIUM" in roles_list:
                UserPremium.objects.create(user=user)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return user
