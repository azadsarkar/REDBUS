from typing import Any
from django.forms import ModelForm
from .models import Bus, BusRoute, BusSchedule, IntermidiateStop, BusBooking
from django.core.exceptions import ValidationError
class BusForm(ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'
    
class BusRoutForm(ModelForm):
    class Meta:
        model = BusRoute
        fields = "__all__"
        

class BusRouteScheduleForm(ModelForm):
    class Meta:
        model = BusSchedule
        fields = "__all__"
        
class IntermidiateStopForm(ModelForm):
    class Meta:
        model = IntermidiateStop
        fields = '__all__'
        


class BusBookingForm(ModelForm):
    class Meta:
        model = BusBooking
        fields = ['id','customer_name', 'customer_email', 'customer_age','gender', 'seats']
        
    def clean_seats(self):
        data = self.cleaned_data['seats']
        if data > 5:
            raise ValidationError('please select lese then 5 seats')
        return data