from django.urls import path, include
from . import views
from account import views as account_views
# app_name = 'account'

urlpatterns = [
   path('home',account_views.home, name= 'home' ),
   path('dashboard/', views.home, name= 'dashboard'),
   path('bus_add/', views.bus, name='add_bus'),
   path('bus_route_add/', views.bus_route, name='bus_route_add'),
   path('update/<int:id>/', views.update_bus_route, name='update_bus_route'),
   path('delete/<int:id>/', views.delete_bus_route, name='delete_bus_route'),
   path('add_bus_schedule/', views.bus_schedule, name='bus_schedule'),
   path('bus_schedul_details/',views.bus_schedule_details, name= 'bus_schedule_details'),
   path('update_schedule/<int:id>/', views.update_schedule, name='update_schedule'),
   path('delete_schedule/<int:id>/', views.delete_schedule, name='delete_schedule'),
]