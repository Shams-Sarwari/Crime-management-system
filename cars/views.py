from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, CarOwner, CarHistory, JawazSayr
from .forms import CreateCarForm, EditCarForm, CreateOwnerForm, JawazForm
from django.http import HttpResponse
from accounts.models import DriverProfile
from accounts.utils import pagination_items
from django.db.models import Q
from datetime import date
# Create your views here.

def car_list(request):
    search_text = ''
    if request.GET.get('search_text'):
        search_text = request.GET.get('search_text')
        cars = Car.objects.distinct().filter(
            Q(plate_number=search_text) |
            Q(engine_num=search_text)
        )
    else:
        cars = Car.objects.all()
    custom_range, cars = pagination_items(request, cars, 10)

    context = {
        'cars': cars,
        'custom_range': custom_range,
        'search_text': search_text,
        'section': 'cars',
    }
    return render(request, 'cars/car_list.html', context)

def car_detail(request, pk):
    car = get_object_or_404(Car, id = pk)
    car_history = car.carhistory_set.all()
    context = {
        'car': car, 
        'history': car_history,
        'section': 'cars'
    }
    return render(request, 'cars/car_detail.html', context)

def create_car(request, pk=None):
    
    if request.method == 'POST':
        form = CreateCarForm(request.POST)
        if form.is_valid():
            if pk:
                driver = DriverProfile.objects.get(id=pk)
                car = form.save(commit=False)
                car.driver = driver
                car.save()
                return redirect('driver-detail', driver.id)
            
            else:
                form.save()
                return redirect('cars:car-list')
    
    else:
        form = CreateCarForm()

    context = {
        'form': form, 
        'section': 'cars',
    }
    return render(request, 'cars/create_car.html', context)

def edit_car(request, pk):
    car = get_object_or_404(Car, id=pk)

    # to create car history
    car_driver = car.driver
    car_owner = car.owner

    form = EditCarForm(instance=car)
    if request.method=='POST':
        form = EditCarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            # create a history if driver or owner has been updated
            if request.POST['driver_licence'] != '':
                if car_driver != DriverProfile.objects.get(licence_num = request.POST['driver_licence']):
                    CarHistory.objects.create(
                        car = car,
                        driver = DriverProfile.objects.get(licence_num = request.POST['driver_licence'])
                    )
            if request.POST['owner_tazkira'] != '':
                if car_owner != CarOwner.objects.get(tazkira_number = request.POST['owner_tazkira']):
                    CarHistory.objects.create(
                        car = car, 
                        owner = CarOwner.objects.get(tazkira_number = request.POST['owner_tazkira'])
                    )
            form.save()
            
            return redirect('cars:car-detail', car.id)
    context = {
        'form': form, 
        'section': 'cars',
    }
    return render(request, 'cars/edit_car.html', context)

def delete_car(request, pk):
    car = get_object_or_404(Car, id=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('cars:car-list')
    context = {
        'car': car, 
        'section': 'cars',
    }
    return render(request, 'cars/delete_car.html', context)


def owner_list(request):
    search_text=''
    if request.GET.get('search_text'):
        search_text = request.GET.get('search_text')
        owners = CarOwner.objects.distinct().filter(
            Q(tazkira_number=search_text)|
            Q(phone_number=search_text)
        )
    else:
        owners = CarOwner.objects.all()
    custom_range, owners = pagination_items(request, owners, 10)

    context = {
        'owners': owners, 
        'custom_range': custom_range,
        'search_text': search_text,
        'section': 'owners',
    }
    return render(request, 'cars/owner_list.html', context)


def owner_detail(request, pk):
    owner = get_object_or_404(CarOwner, id=pk)
    context = {
        'owner': owner, 
        'section': 'owners',
    }
    return render(request, 'cars/owner_detail.html', context)


def create_owner(request):
    
    if request.method == 'POST':
        form = CreateOwnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cars:owner-list')
    else: 
        form = CreateOwnerForm()
    
    context = {
        'form': form, 
        'section': 'owners',
    }
    return render(request, 'cars/create_owner.html', context)

def update_owner(request, pk):
    owner = get_object_or_404(CarOwner, id=pk)
    form = CreateOwnerForm(instance=owner)
    if request.method == 'POST':
        form = CreateOwnerForm(request.POST, request.FILES, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('cars:owner-detail', owner.id)

    context = {
        'form': form, 
        'section': 'owners',
    }
    return render(request, 'cars/update_owner.html', context)

def delete_owner(request, pk):
    owner = CarOwner.objects.get(id = pk)
    if request.method == 'POST':
        owner.delete()
        return redirect('cars:owner-list')
    
    context = {
        'owner': owner, 
        'section': 'owners',
    }
    return render(request, 'cars/delete_owner.html', context)

def create_jawaz(request, pk):
    car = get_object_or_404(Car, id=pk)
    try:
        driver = car.driver
    except: 
        driver = None
    if request.method == 'POST':
        form = JawazForm(request.POST)
        if form.is_valid():
            jawaz = form.save(commit=False)
            jawaz.car = car
            jawaz.driver = driver
            jawaz.verified_by = request.user.staffprofile
            jawaz.created = date.today()
            jawaz.save()
            return redirect('cars:car-detail', car.id)
        else: 
            print(form.errors)

    else:
        form = JawazForm()
    
    context = {
        'form': form
    }
    return render(request, 'cars/create_jawaz.html', context)

def jawaz_list(request):
    jawazs = JawazSayr.objects.all()
    context = {
        'jawazs': jawazs
    }
    return render(request, 'cars/jawaz_list.html', context)

def jawaz_detail(request, pk):
    jawaz = JawazSayr.objects.get(id=pk)
    context = {
        'jawaz': jawaz
    }
    return render(request, 'cars/jawaz_detail.html', context)


def update_jawaz(request, pk):
    jawaz = get_object_or_404(JawazSayr, id=pk)
    form = JawazForm(instance=jawaz)
    if request.method == 'POST':
        form = JawazForm(request.POST, instance=jawaz)
        if form.is_valid():
            form.save()
            return redirect('driver-detail', jawaz.driver.id)
    
    context = {
        'form': form
    }
    return render(request, 'cars/create_jawaz.html', context)