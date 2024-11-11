from django.forms import ModelForm
from .models import Bus, BusRoute
class BusForm(ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'
    
class BusRoutForm(ModelForm):
    class Meta:
        model = BusRoute
        fields = "__all__"