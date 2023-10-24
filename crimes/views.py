from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateCrimeForm, CreateCarCrimeForm
from .models import Crime, CarCrime, Payment
from accounts.models import DriverProfile
from cars.models import Car
from accounts.models import StaffProfile
from django.contrib import messages


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
    crimes = CarCrime.objects.all()
    context = {
        'crimes': crimes
    }
    return render(request, 'crimes/driver_crime_list.html', context)

def create_car_crime(request):
    profile = StaffProfile.objects.get(user = request.user)
    if request.method == 'POST':
        form = CreateCarCrimeForm(request.POST)
        if form.is_valid():
            plate = form.cleaned_data['plate_num']
            car = get_object_or_404(Car, plate_number = plate)
            crime = form.save(commit=False)
            crime.stuff = profile
            crime.car = car
            crime.save()
            return redirect('crimes:driver-crime-list')
    else: 
        form = CreateCarCrimeForm()

    context = {
        'form': form
    }
    return render(request, 'crimes/create_driver_crime.html', context)

def log_payment(request, pk):
    driver = DriverProfile.objects.get(id=pk)
    total = 0
    if request.method == 'POST':
        paid_crimes = request.POST.getlist('paid_crimes')
        car_crimes = []
        for i in paid_crimes:
            crime = CarCrime.objects.get(id=int(i))
            total += crime.price + crime.expiry_fine
            crime.paid = True
            crime.save()
            car_crimes.append(crime)
        
        messages.success(request, 'جرایم موفقانه پرداخت گردید')
        
    # first create the log and then add car crimes to this log
    log = Payment.objects.create(
        staff = request.user.staffprofile,
        driver = driver,
        price = total,
    )
    log.save()

    for item in car_crimes:
        item.payment = log
        item.save()
    
    return redirect('driver-detail', driver.id)
