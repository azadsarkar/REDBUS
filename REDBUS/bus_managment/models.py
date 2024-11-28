from django.db import models
from account.models import User
from django.db.models import Avg

# Create your models here.


class Bus(models.Model):
    BUS_TYPE = (("ac", "AC"), ("non-ac", "NON-AC"))
    bus_name = models.CharField(max_length=30)
    bus_type = models.CharField(max_length=10, choices=BUS_TYPE)
    bus_capacity = models.IntegerField()
    
    

    def __str__(self):
        return f"{self.bus_name} {self.bus_type} {self.bus_capacity}"


class BusRoute(models.Model):
    bus_rout = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bus')
    sourse = models.CharField(max_length=20)
    destinations = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.sourse} {self.destinations}"


class BusSchedule(models.Model):
    bus_route_schedule = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='bus_route')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True)
    department_time = models.TimeField()
    arrivale_time = models.TimeField()
    tickit_price = models.IntegerField()
    avalable_seates = models.IntegerField()
    

    def __str__(self):
        return f"{self.bus.bus_name} ({self.department_time} To {self.arrivale_time})"


class IntermidiateStop(models.Model):
    
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='intermidiate_stop')
    stop_name = models.CharField(max_length=20)
    intermidiate_stop_time = models.DateTimeField(null=True, blank=True)
    inter_stop_id = models.IntegerField(unique=True)
    
    
    def __str__(self):
        return f'{self.stop_name} {self.inter_stop_id}'
    
    
class BusBooking(models.Model):
    GENDER_TYPE =(("M","Male"),('F','Female'))
    PAYMENT_STATUS = (('panding','Panding'),('success','Success'),('cancle','Cancle'),('refund','Refund'))
    bus_schedule = models.ForeignKey(BusSchedule,on_delete=models.CASCADE, null=True, blank= True, related_name='schedule')
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='bus_booking')
    customer_name = models.CharField(max_length=30, null=False)
    customer_age = models.IntegerField()
    customer_email = models.EmailField(max_length=30)
    gender = models.CharField(max_length=10, choices = GENDER_TYPE)
    seats = models.IntegerField(null=True, blank=True)
    selected_seats = models.CharField(max_length=255, null=True, blank=True)
    booking_date = models.DateField(auto_now_add=True, null=True, blank=True)
    payment_status = models.CharField(choices = PAYMENT_STATUS, max_length=20, default="panding")
    payment_intent_id = models.CharField(max_length=250, null=True, blank=True)
    
    def total_payment(self):
        return (self.seats * self.bus_schedule.tickit_price)
    
    def __str__(self):
        return f'{self.customer_name}{self.customer_email}{self.seats}'


class Payment(models.Model):
    bus_booking = models.ForeignKey(BusBooking, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')
    payment_ammount = models.IntegerField()
    payment_method = models.CharField(max_length=20)
    cancellation_date = models.DateTimeField()
    payment_status = models.CharField(choices=BusBooking.PAYMENT_STATUS, max_length=20)
    cancellation_reason = models.TextField()
    
    def __str__(self):
        return f'{self.cancellation_date}{self.payment_method}{self.payment_status}'
    
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='feedback')
    booking = models.ForeignKey(BusBooking, on_delete=models.CASCADE, related_name='booking')
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE, related_name='bus_schedule',null=True, blank=True)
    safety = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    cleanness = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    staff_behaviour = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    time_punctuality = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comfort = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    feedback_date = models.DateTimeField(auto_now_add=True)
    
    def average_ratting(self):
        average = ((self.safety) + (self.cleanness) + (self.staff_behaviour) + (self.time_punctuality) + (self.comfort)) / 5
        return round(average,1)
    
    def __str__(self):
        return f'{self.user}{self.average_ratting()}'