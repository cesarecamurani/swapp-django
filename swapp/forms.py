import pdb

from django.forms import *
from django.contrib.auth.models import User

from swapp.models.item import Item
from swapp.models.profile import Profile
from swapp.models.donation import Donation
from swapp.models.swapp_request import SwappRequest
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


class ProfileCreateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'city', 'country', 'address']

    def __init__(self, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs = {
                'class': 'form-control', 'placeholder': field.label, 'autocomplete': 'off'
            }


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = CharField(widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'}))
    password = CharField(widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'off'}))


class ChangePasswordForm(Form):
    username = CharField(widget=TextInput())
    old_password = CharField(widget=PasswordInput())
    new_password = CharField(widget=PasswordInput())
    new_password_confirmation = CharField(widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'}
        )
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


class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'picture']

    def __init__(self, *args, **kwargs):
        super(ItemCreateForm, self).__init__(*args, **kwargs)

    name = CharField(widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name', 'autocomplete': 'off'}))
    description = CharField(widget=Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description', 'autocomplete': 'off'}))
    picture = ImageField(widget=ClearableFileInput(
        attrs={'class': 'form-control', 'type': 'file'}))


class SwappRequestCreateForm(ModelForm):
    class Meta:
        model = SwappRequest
        fields = ['offered_product']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(SwappRequestCreateForm, self).__init__(*args, **kwargs)

        self.fields['offered_product'].widget = Select(
            choices=Item.objects.all().filter(owner=user).values_list('id', 'name'),
            attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'}
        )


class DonationCreateForm(ModelForm):
    class Meta:
        model = Donation
        fields = []
