from django.db import models

# Create your models here.


class Bus(models.Model):
    BUS_TYPE = (("ac", "AC"), ("non-ac", "NON-AC"))
    bus_name = models.CharField(max_length=30)
    bus_type = models.CharField(max_length=10, choices=BUS_TYPE)
    bus_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.bus_name} {self.bus_type} {self.bus_capacity}"


class BusRoute(models.Model):
    bus_rout = models.ForeignKey(Bus, on_delete=models.CASCADE)
    sourse = models.CharField(max_length=20)
    destinations = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.sourse} {self.destinations}"


class BusSchedule(models.Model):
    bus_route_schedule = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True)
    department_time = models.TimeField()
    arrivale_time = models.TimeField()
    tickit_price = models.IntegerField()
    avalable_seates = models.IntegerField()

    def __str__(self):
        return f"{self.department_time} {self.arrivale_time} {self.tickit_price} {self.avalable_seates}"


class IntermidiateStop(models.Model):
    
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    stop_name = models.CharField(max_length=20)
    intermidiate_stop_time = models.DateTimeField(null=True, blank=True)
    inter_stop_id = models.IntegerField(unique=True)
    
    
    def __str__(self):
        return f'{self.stop_name} {self.inter_stop_id}'
    