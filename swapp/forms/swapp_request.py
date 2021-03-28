from django.forms import *
from swapp.models.item import Item
from swapp.models.swapp_request import SwappRequest


class SwappRequestCreateForm(ModelForm):
    class Meta:
        model = SwappRequest
        fields = ['offered_product']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(SwappRequestCreateForm, self).__init__(*args, **kwargs)

        self.fields['offered_product'].widget = Select(
            choices=Item.objects.all().filter(owner=user, donated=False, removed=False, out_for_request=False).values_list('id', 'name'),
            attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'}
        )
