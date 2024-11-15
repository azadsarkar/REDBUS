from django.contrib import admin
from .models import Bus, BusRoute, BusSchedule, IntermidiateStop
# Register your models here.
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus_name', 'bus_type', 'bus_capacity']
 
    
@admin.register(BusRoute)
class BusRoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'sourse', 'destinations', 'bus_rout']
    
@admin.register(BusSchedule)
class BusScheduleAdmmin(admin.ModelAdmin):
    list_display = ['id', 'bus_route_schedule','bus', 'department_time', 'arrivale_time', 'tickit_price', 'avalable_seates']
    
@admin.register(IntermidiateStop)
class IntermidiateStopAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus_route', 'stop_name','intermidiate_stop_time', 'inter_stop_id']
    
