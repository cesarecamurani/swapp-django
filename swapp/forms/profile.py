from django.forms import *
from swapp.models.profile import Profile


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
