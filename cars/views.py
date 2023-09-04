from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, CarOwner
from .forms import CreateCarForm, EditCarForm, CreateOwnerForm
from django.http import HttpResponse
from accounts.models import DriverProfile
# Create your views here.

def car_list(request):
    cars = Car.objects.all()
    context = {
        'cars': cars
    }
    return render(request, 'cars/car_list.html', context)

def car_detail(request, pk):
    car = get_object_or_404(Car, id = pk)
    context = {
        'car': car
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
    form = EditCarForm(instance=car)
    if request.method=='POST':
        form = EditCarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
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
    owners = CarOwner.objects.all()
    context = {
        'owners': owners
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