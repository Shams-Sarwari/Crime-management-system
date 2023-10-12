from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, CarOwner, CarHistory
from .forms import CreateCarForm, EditCarForm, CreateOwnerForm
from django.http import HttpResponse
from accounts.models import DriverProfile
from accounts.utils import pagination_items
from django.db.models import Q
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
    }
    return render(request, 'cars/car_list.html', context)

def car_detail(request, pk):
    car = get_object_or_404(Car, id = pk)
    car_history = car.carhistory_set.all()
    context = {
        'car': car, 
        'history': car_history
    }
    return render(request, 'cars/car_detail.html', context)

def create_car(request):
    
    if request.method == 'POST':
        form = CreateCarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cars:car-list')
    
    else:
        form = CreateCarForm()

    context = {
        'form': form
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
        'form': form
    }
    return render(request, 'cars/edit_car.html', context)

def delete_car(request, pk):
    car = get_object_or_404(Car, id=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('cars:car-list')
    context = {
        'car': car
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
    }
    return render(request, 'cars/owner_list.html', context)


def owner_detail(request, pk):
    owner = get_object_or_404(CarOwner, id=pk)
    context = {
        'owner': owner
    }
    return render(request, 'cars/owner_detail.html', context)


def create_owner(request):
    
    if request.method == 'POST':
        form = CreateOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cars:owner-list')
    else: 
        form = CreateOwnerForm()
    
    context = {
        'form': form
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
        'form': form
    }
    return render(request, 'cars/update_owner.html', context)

def delete_owner(request, pk):
    owner = CarOwner.objects.get(id = pk)
    if request.method == 'POST':
        owner.delete()
        return redirect('cars:owner-list')
    
    context = {
        'owner': owner
    }
    return render(request, 'cars/delete_owner.html', context)