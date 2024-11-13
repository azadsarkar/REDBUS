from django.urls import path, include
from . import views
urlpatterns = [
   path('dashboard/', views.home, name= 'dashboard'),
   path('bus_add/', views.bus, name='add_bus'),
   path('bus_route_add/', views.bus_route, name='bus_route_add'),
   path('update/<int:id>/', views.update_bus_route, name='update_bus_route'),
   path('delete/<int:id>/', views.delete_bus_route, name='delete_bus_route'),
]
