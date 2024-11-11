from django.urls import path, include
from . import views
urlpatterns = [
   
   path('bus_add/', views.bus, name='add_bus')
]
