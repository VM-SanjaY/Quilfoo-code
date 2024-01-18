from django.forms import ModelForm
from .models import UserPost
from loginapp.models import Websiteuser

class UserPostForm(ModelForm):
    class Meta:
        model=UserPost
        fields = ['description']


class WebsiteuserForm(ModelForm):
    class Meta:
        model = Websiteuser
        fields = ['bio']