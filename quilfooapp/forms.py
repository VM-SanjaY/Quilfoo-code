from django.forms import ModelForm
from loginapp.models import Websiteuser

class WebsiteuserForm(ModelForm):
    class Meta:
        model = Websiteuser
        fields = ['bio']