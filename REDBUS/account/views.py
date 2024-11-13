from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from .forms import CustomerSignupForm
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from .forms import PasswordResetForm
from django.contrib.auth.models import User 
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView

def home(request):
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        if request.user.is_superuser == True:
            return render(request, 'bus_managment/dashbord.html')
        
        return render(request, 'base.html')
    
"""user Sign in form Class based View """

class CustomerRegistration(TemplateView):
    
    template_name = 'account/Signin.html'  
    def get(self, request, *args, **kwargs):
        
        fm = CustomerSignupForm() 
        
        return render(request, self.template_name, {'form': fm})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        fm = CustomerSignupForm(request.POST)  
        if fm.is_valid():
            fm.save()  
            messages.success(request, 'User registered successfully.')
            return redirect('home')
        else:  
            return render(request, self.template_name, {'form': fm})
        
"""USer Login class based Views"""


class UserLogin(View):  
    def get(self, request):
        if not request.user.is_authenticated:
            form = AuthenticationForm()
            return render(request, 'account/login.html', {'form': form, 'user': request.user})
        else:
            # return redirect('home')
            if request.user.is_superuser == True:
                
                   return redirect('deshbord')
            else:
                return redirect('home')
            
    def post(self, request):
        if not request.user.is_authenticated:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user is not None and user.is_superuser == True:
                    auth.login(request, user)
                    # messages.success(request, 'You are Logged in')
                    return redirect('dashboard')
                # messages.success(request, 'You are Logged in')
                login(request, user)
                return redirect('home') 
            else:
                return render(request, 'account/login.html', {'form': form})
            
        else:
            # messages.info(request, 'you are already logged in')
            return redirect('home')
        
        
"""user logout function """  

 
def user_log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def desh_bord(request):
    return render(request, 'bus_managment/dashbord.html')

def contact(request):
    return render(request, 'contact.html')

class UpdateTemplateView(TemplateView):
    template_name = 'base.html'
    
    
class UserUpdateView(UpdateView):
    template_name = 'account/user_update.html'
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = '/updateTemplatevie/'
    
    

class UserDeleteViews(DeleteView):
    model = User
    template_name = 'account/user_confirm_delete.html'
    success_url = '/signup/'