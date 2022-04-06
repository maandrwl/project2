
from dataclasses import field
from pyexpat import model
from django.forms import ModelForm
from .models import Item,Assign


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class AssignForm(ModelForm):
    class Meta:
        model = Assign
        fields = '__all__'