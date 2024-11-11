from django.shortcuts import render
from .forms import BusForm, BusRoutForm
# Create your views here.
def bus(request):
    fm = BusForm()
    fm1 = BusRoutForm()
    return render(request, 'bus_managment/add_bus.html', {'form':fm,'form1':fm1})