from django.forms import *
from swapp.models.donation import Donation


class DonationCreateForm(ModelForm):
    class Meta:
        model = Donation
        fields = []
