from django.forms import ModelForm, widgets
from . import models

class CityForm(ModelForm):
    model = models.City
    fields = ['name',]
    widgets = {
            'name': widgets.TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        }
