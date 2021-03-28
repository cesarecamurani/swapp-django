from django.forms import *
from swapp.models.item import Item


class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'current_location', 'preferred_change', 'picture']

    def __init__(self, *args, **kwargs):
        super(ItemCreateForm, self).__init__(*args, **kwargs)

    name = CharField(widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name', 'autocomplete': 'off'}))
    current_location = CharField(widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Current Location', 'autocomplete': 'off'}))
    preferred_change = CharField(widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Preferred Item or Service to be swapped with', 'autocomplete': 'off'}))
    description = CharField(widget=Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description (Max 100 characters)', 'autocomplete': 'off'}))
    picture = ImageField(widget=ClearableFileInput(
        attrs={'class': 'form-control', 'type': 'file'}))
