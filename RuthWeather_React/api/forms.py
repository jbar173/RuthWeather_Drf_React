from django.forms import ModelForm, ModelChoiceField, widgets
from . import models


# class UpdateReportForm(ModelForm):
#
#     city = ModelChoiceField(queryset=models.City.objects.all())
#
#     class Meta:
#         model = models.Report
#         fields = ['city',]


# class CreateCityForm(ModelForm):
#     model = models.City
#     fields = ['name',]
#     widgets = {
#         'name': widgets.TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
#     }
