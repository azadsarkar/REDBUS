from django.db import models

# Create your models here.

class Bus(models.Model):
    BUS_TYPE = (
        ('ac','AC'),
        ('non-ac','NON-AC')
    )
    bus_name = models.CharField(max_length=30)
    bus_type = models.CharField(max_length=10, choices=BUS_TYPE)
    bus_capacity = models.IntegerField()
    
    def __str__(self):
        return f'{self.bus_name} {self.bus_type} {self.bus_capacity}'
    
    
class BusRoute(models.Model):
    bus_rout = models.ForeignKey(Bus, on_delete = models.CASCADE)
    sourse = models.CharField(max_length=20)
    destinations = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.sourse} {self.destinations}'
    
