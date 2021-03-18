from django.forms import ModelForm
from django.contrib.auth.models import User
from swapp.models.profile import Profile

class UserCreateForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class ProfileCreateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'city', 'country', 'address')
