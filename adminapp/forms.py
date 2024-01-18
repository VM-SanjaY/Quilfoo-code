from django.forms import ModelForm
from loginapp.models import Websiteuser
from .models import AgreementData


class WebsiteuserForm(ModelForm):
    class Meta:
        model = Websiteuser
        fields = ['bio']


class AgreementdetailForm(ModelForm):
    class Meta:
        model = AgreementData
        fields = ['description']
