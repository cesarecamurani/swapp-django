from django.forms import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from swapp.models.profile import Profile


class ProfileCreateForm(ModelForm):
    country = CountryField(blank_label='Select Country',).formfield()

    class Meta:
        model = Profile
        fields = ['phone_number', 'city', 'country', 'address']
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs = {
                'class': 'form-control', 'placeholder': field.label, 'autocomplete': 'off'
            }
