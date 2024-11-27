from django.contrib import admin
from .models import Bus, BusRoute, BusSchedule, IntermidiateStop, BusBooking, Payment, Feedback


# Register your models here.
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ["id", "bus_name", "bus_type", "bus_capacity"]


@admin.register(BusRoute)
class BusRoutAdmin(admin.ModelAdmin):
    list_display = ["id", "sourse", "destinations", "bus_rout"]


@admin.register(BusSchedule)
class BusScheduleAdmmin(admin.ModelAdmin):
    list_display = [
        "id",
        "bus_route_schedule",
        "bus",
        "department_time",
        "arrivale_time",
        "tickit_price",
        "avalable_seates",
    ]


@admin.register(IntermidiateStop)
class IntermidiateStopAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "bus_route",
        "stop_name",
        "intermidiate_stop_time",
        "inter_stop_id",
    ]


@admin.register(BusBooking)
class BusBookingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer_name",
        "customer_age",
        "booking_date",
        "user",
        "customer_email",
        "gender",
        "seats",
        "payment_status",
        "bus_schedule",
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "bus_booking",
        "payment_ammount",
        "payment_method",
        "cancellation_date",
        "payment_status",
        "cancellation_reason",
    ]


@admin.register(Feedback)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'booking','bus_schedule', 'average_ratting', 'feedback_date']
    
    # def bus_name(self, obj):
    #     return obj.booking.bus_schedule.bus.bus_name