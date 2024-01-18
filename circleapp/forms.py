from django.forms import ModelForm
from loginapp.models import Websiteuser,Circle

class CircleForm(ModelForm):
    class Meta:
        model = Circle
        fields = ['description']