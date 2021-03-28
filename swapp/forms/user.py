from django.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserCreateForm(ModelForm):
    password = CharField(widget=PasswordInput())
    password_confirmation = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs = {
                'class': 'form-control', 'placeholder': field.label, 'autocomplete': 'off'
            }

        self.fields['password'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
        self.fields['password_confirmation'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}
        )

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            self.add_error('password_confirmation', "Password does not match")

        return cleaned_data


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = CharField(widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'}))
    password = CharField(widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'off'}))


class ChangePasswordForm(Form):
    old_password = CharField(widget=PasswordInput())
    new_password = CharField(widget=PasswordInput())
    new_password_confirmation = CharField(widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Old password', 'autocomplete': 'off'}
        )
        self.fields['new_password'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New password', 'autocomplete': 'off'}
        )
        self.fields['new_password_confirmation'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm new password', 'autocomplete': 'off'}
        )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirmation = cleaned_data.get('new_password_confirmation')

        if new_password != new_password_confirmation:
            self.add_error('new_password_confirmation', 'Password does not match')

        return cleaned_data
