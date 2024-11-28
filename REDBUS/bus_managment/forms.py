from typing import Any
from django.forms import ModelForm
from .models import Bus, BusRoute, BusSchedule, IntermidiateStop, BusBooking, Payment, Feedback
from django.core.exceptions import ValidationError
from django import forms
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
        fields = ['id','customer_name', 'customer_email', 'customer_age','gender', 'seats','selected_seats']
        
    selected_seats = forms.CharField(widget=forms.HiddenInput()) 
        

    

class PaymentCancleForm(ModelForm):
    class Meta:
        model = Payment
        fields = [ 'payment_method', 'cancellation_date', 'cancellation_reason']
        
    cancellation_date = forms.DateTimeField(
    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
)
    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['safety', 'cleanness', 'staff_behaviour', 'time_punctuality', 'comfort', 'comment']
        widgets = {
            'safety': forms.Select(choices=Feedback._meta.get_field('safety').choices),
            'cleanness': forms.Select(choices=Feedback._meta.get_field('cleanness').choices),
            'staff_behaviour': forms.Select(choices=Feedback._meta.get_field('staff_behaviour').choices),
            'time_punctuality': forms.Select(choices=Feedback._meta.get_field('time_punctuality').choices),
            'comfort': forms.Select(choices=Feedback._meta.get_field('comfort').choices),
        }