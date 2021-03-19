from django.forms import *
from django.contrib.auth.models import User
from swapp.models.profile import Profile


class UserCreateForm(ModelForm):
    password = CharField(widget=PasswordInput())
    password_confirmation = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        super().__init__()
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs = {
                'autocomplete': 'off', 'class': 'form-control', 'placeholder': field.label
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


class ProfileCreateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'city', 'country', 'address')

    def __init__(self, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)

        super().__init__()
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs = {
                'autocomplete': 'off', 'class': 'form-control', 'placeholder': field.label
            }
