from django.shortcuts import render, redirect
from .forms import CreateCrimeForm, CreateDriverCrimeForm
from .models import Crime, DriverCrime
from accounts.models import StaffProfile
# Create your views here.
def create_crime(request):
    if request.method == 'POST':
        form = CreateCrimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crimes:crime-list')

    else:
        form = CreateCrimeForm()

    context = {
        'form': form
    }
    return render(request, 'crimes/create_crime.html', context)


def crime_list(request):
    crimes = Crime.objects.all()
    context = {
        'crimes': crimes
    }
    return render(request, 'crimes/crime_list.html', context)

def update_crime(request, pk):
    crime = Crime.objects.get(id=pk)
    form = CreateCrimeForm(instance=crime)
    if request.method == 'POST':
        form = CreateCrimeForm(request.POST, instance=crime)
        if form.is_valid():
            form.save()
            return redirect('crimes:crime-list')
        
    context = {
        'form': form
    }
    return render(request, 'crimes/create_crime.html', context)

def delete_crime(request, pk):
    crime = Crime.objects.get(id=pk)
    if request.method == 'POST':
        crime.delete()
        return redirect('crimes:crime-list')

    context = {
        'crime': crime
    }
    return render(request, 'crimes/delete_crime.html', context)


def driver_crime_list(request):
    crimes = DriverCrime.objects.all()
    context = {
        'crimes': crimes
    }
    return render(request, 'crimes/driver_crime_list.html', context)

def create_driver_crime(request):
    profile = StaffProfile.objects.get(user = request.user)
    if request.method == 'POST':
        form = CreateDriverCrimeForm(request.POST)
        if form.is_valid():
            crime = form.save(commit=False)
            crime.stuff = profile
            crime.save()
            return redirect('crimes:driver-crime-list')
    else: 
        form = CreateDriverCrimeForm()

    context = {
        'form': form
    }
    return render(request, 'crimes/create_driver_crime.html', context)
