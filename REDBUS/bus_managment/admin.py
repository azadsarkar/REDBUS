from django.contrib import admin
from .models import Bus, BusRoute
# Register your models here.
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus_name', 'bus_type', 'bus_capacity']
    
@admin.register(BusRoute)
class BusRoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'sourse', 'destinations', 'bus_rout']