from django.shortcuts import render, get_object_or_404, redirect
from .models import DriverProfile, StaffProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import CustomDriverUserCreationForm, DriverEditForm, AddressForm
from django.urls import reverse
# Create your views here.
def home(request):
    return render(request, 'home.html')


def driver_list(request):
    drivers = DriverProfile.objects.all()
    context = {
        'drivers': drivers,
    }
    return render(request, 'accounts/driver_list.html', context)


def driver_detail(request, pk):
    driver = get_object_or_404(DriverProfile, id=pk)
    context = {
        'driver': driver
    }
    return render(request, 'accounts/driver_detail.html', context)

def staff_list(request):
    staff_list = StaffProfile.objects.all()
    context = {
        'staff_list': staff_list,
    }
    return render(request, 'accounts/staff_list.html', context)

def staff_detail(request, pk):
    staff = get_object_or_404(StaffProfile, id=pk)
    context = {
        'staff': staff,
    }
    return render(request, 'accounts/staff_detail.html', context)

def login_user(request):
    noexist_message = None
    wrong_message = None
    check_user = None

    if request.user.is_authenticated:
        return redirect('accounts:driver_list')

    if request.method == 'POST':
        if request.POST['type'] == 'driver':

            licence_or_email = request.POST['license_or_email']
            password = request.POST['password']

            try:
                driver = DriverProfile.objects.get(licence_num = licence_or_email)
                
            except:
                noexist_message = 'Username does not exist'
                return render(request, 'accounts/login.html', {
                    'noexist_message': noexist_message,
                })
               
            check_user = authenticate(request, username=licence_or_email, password=password)

            if check_user is not None:
                login(request, check_user)
                return redirect('accounts:home')
            else: 
                wrong_message = 'Username or password is incorrect'
        
        elif request.POST['type'] == 'staff':

            licence_or_email = request.POST['license_or_email']
            password = request.POST['password']

            try:
                staff = get_user_model().objects.get(email = licence_or_email)
            except:    
                noexist_message = 'User does not exist'
                return render(request, 'accounts/login.html', {
                    'noexist_message': noexist_message,
                })           
            check_user = authenticate(request, username=licence_or_email, password=password)
            
            if check_user is not None:
                login(request, check_user)
                return redirect('accounts:home')
            else: 
                wrong_message = 'Username or password is incorrect'


    context = {
        'noexist_message': noexist_message,
        'wrong_message': wrong_message,
    }
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('accounts:login')



def register_driver(request):
    
    if request.method == 'POST':
        form = CustomDriverUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_driver = True
            user.save()
            driver = DriverProfile.objects.get(user=user)
            return redirect('accounts:edit-driver-profile', driver.id)

            
    else:
        form = CustomDriverUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register_driver.html', context)


def edit_driver_profile(request, pk):
    profile = DriverProfile.objects.get(id = pk)
    form = DriverEditForm(instance=profile)
    if profile.current_address is not None:
        add_form = AddressForm(instance=profile.current_address)
    else: 
        add_form = AddressForm()

    if request.method == 'POST':
        form = DriverEditForm(request.POST, request.FILES, instance=profile)
        add_form = AddressForm(request.POST)
        if form.is_valid() and add_form.is_valid():
            address = add_form.save()
            profile = form.save(commit=False)
            profile.current_address = address
            profile.save()
            return redirect('accounts:driver-detail', profile.id)


    context = {
        'form': form, 
        'add_form': add_form,
    }
    return render(request, 'accounts/edit_driver_profile.html', context)
