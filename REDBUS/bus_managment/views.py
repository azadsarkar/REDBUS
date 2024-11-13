from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from .forms import BusForm, BusRoutForm
from .models import BusRoute


def home(request):
    data = BusRoute.objects.all()
    return render(request, 'bus_managment/dashbord.html',{'data':data})

def bus(request):  
    
    if request.method == "GET":
        fm = BusForm() 
        return render(request, 'bus_managment/add_bus.html', {'form': fm})

    if request.method == "POST":
        fm = BusForm(request.POST)  
        if fm.is_valid():  
            fm.save()
            return redirect('bus_route_add')
        
        
def bus_route(request):
    if  request.method == "GET":
        fm = BusRoutForm()
        return render(request, 'bus_managment/add_bus_route.html', {'form1':fm})
    
    if request.method == "POST":
        fm = BusRoutForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('add_bus')
        
        
def update_bus_route(request, id):
    bus_route = get_object_or_404(BusRoute, id=id)
    
    if request.method == 'POST':
        form = BusRoutForm(request.POST, instance=bus_route)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Or another redirect after saving
    else:
        form = BusRoutForm(instance=bus_route)
    
    return render(request, 'bus_managment/update_bus_route.html', {'form': form})

def delete_bus_route(request, id):
    bus_route = get_object_or_404(BusRoute, id=id)
    
    if request.method == 'POST':
        bus_route.delete()
        return redirect('dashboard')  
    
    return render(request, 'bus_managment/confirm_delete.html', {'bus_route': bus_route})