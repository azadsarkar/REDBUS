from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from .forms import BusForm, BusRoutForm, BusRouteScheduleForm, IntermidiateStopForm
from .models import BusRoute, BusSchedule, IntermidiateStop
from django.core.paginator import Paginator


def home(request):
    if request.user.is_superuser and request.user.is_authenticated:
        all_data = BusRoute.objects.all().order_by('id')
        paginator = Paginator(all_data,5, orphans=1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'bus_managment/dashbord.html',{'data':page_obj})
    else:
        return redirect("home")


def bus(request):  
    if request.user.is_superuser and request.user.is_authenticated:
        if request.method == "GET":
            fm = BusForm() 
            return render(request, 'bus_managment/add_bus.html', {'form': fm})

        if request.method == "POST":
            fm = BusForm(request.POST)  
            if fm.is_valid():  
                fm.save()
                return redirect('bus_route_add')
    else:
        return redirect("home")
        
        
def bus_route(request):
    if request.user.is_superuser and request.user.is_authenticated:
        if  request.method == "GET":
            fm = BusRoutForm()
            return render(request, 'bus_managment/add_bus_route.html', {'form1':fm})
        
        if request.method == "POST":
            fm = BusRoutForm(request.POST)
            if fm.is_valid():
                fm.save()
                return redirect('add_bus')
    else:
        return redirect("home")
        
        
def update_bus_route(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        bus_route = get_object_or_404(BusRoute, id=id)
        
        if request.method == 'POST':
            form = BusRoutForm(request.POST, instance=bus_route)
            if form.is_valid():
                form.save()
                return redirect('dashboard')  # Or another redirect after saving
        else:
            form = BusRoutForm(instance=bus_route)
        
        return render(request, 'bus_managment/update_bus_route.html', {'form': form})
    
    else:
        return redirect("home")
        
        
def delete_bus_route(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        bus_route = get_object_or_404(BusRoute, id=id)
        
        if request.method == 'POST':
            bus_route.delete()
            return redirect('dashboard')  
        
        return render(request, 'bus_managment/confirm_delete.html', {'bus_route': bus_route})

    else:
        return redirect("home")
   
 
def bus_schedule(request):
    if request.user.is_superuser and request.user.is_authenticated:
        if request.method == "POST":
            fm = BusRouteScheduleForm(request.POST)
          
            if fm.is_valid():
                fm.save()
                return redirect('dashboard')
            
            else:
                return redirect("bus_schedule")
            
        else:
            fm = BusRouteScheduleForm()
            return render(request, 'bus_managment/bus_schedule.html', {"form":fm})
    else:
        return redirect("home")
    

def bus_schedule_details(request):
    if request.user.is_superuser and request.user.is_authenticated:
        data = BusSchedule.objects.all()  # Fetch all bus schedule records
        bus_schedule_data = []
        for schedule in data:
            # Access the related BusRoute fields
            bus_route = schedule.bus_route_schedule
            sourse = bus_route.sourse
            destinations = bus_route.destinations
            # Retrieve all intermediate stops for this BusRoute
            inter_stops = IntermidiateStop.objects.filter(bus_route=bus_route)
            
            # Add the relevant data to the list
            bus_schedule_data.append({
                'schedule': schedule,
                'sourse': sourse,
                'destinations': destinations,
                'inter_stops': inter_stops,
            })
            
        # all_data = BusRoute.objects.all().order_by('id')
        paginator = Paginator(bus_schedule_data,5, orphans=1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        # Pass the data to the template
        return render(request, 'bus_managment/bus_schedul_details.html', {
            'bus_schedule_data': page_obj,
        })
    else:
        return redirect("home")
    

def update_schedule(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        bus_schedule = get_object_or_404(BusSchedule, id=id)
        if request.method == 'POST':
            form = BusRouteScheduleForm(request.POST, instance=bus_schedule)
            if form.is_valid():
                form.save()
                return redirect('bus_schedule_details')  # Redirect to the schedule list page
        else:
            form = BusRouteScheduleForm(instance=bus_schedule)
        return render(request, 'bus_managment/update_schedule.html', {'form': form})

    else:
        return redirect("home")
 
    
def delete_schedule(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        bus_schedule = get_object_or_404(BusSchedule, id=id)
        bus_schedule.delete()
        return redirect('bus_schedule_details') 
    
    else:
        return redirect("home")
    
    
def intermidiate_stop(request):
    if request.method == "GET":
        fm = IntermidiateStopForm()
        return render(request, "bus_managment/intermidiate.html", {'form':fm})
    
    if request.method == "POST":
        fm = IntermidiateStopForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect("intermidiate")
        else:
            return redirect('dashboard')