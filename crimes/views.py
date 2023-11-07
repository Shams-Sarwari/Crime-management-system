from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateCrimeForm, CreateCarCrimeForm
from .models import Crime, CarCrime, Payment
from accounts.models import DriverProfile
from cars.models import Car
from accounts.models import StaffProfile
from django.contrib import messages
from datetime import date, timedelta

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
    all_crimes = Crime.objects.all()
    crime_list = []
    for item in all_crimes:
        crime_list.append(item.title)

    
    if request.method == 'POST':
        plate = request.POST.get('plate')
        try:
            car = Car.objects.get(plate_number=plate)
            
        except:
            messages.error(request, 'پلیت نمبر وارد شده در سیستم موجود نیست')
            return redirect('crimes:fine-driver')
        try:
            crime = Crime.objects.get(title=request.POST.get('crime_type'))
        except:
            messages.error(request, 'لطفا نوعیت جریمه را از لیست بدون تغییر انتخاب کنید')
            return redirect('crimes:fine-driver')
        
        price = request.POST.get('price')

        location = None
        if request.POST.get('location'):
            location = request.POST.get('location')

        paid = False
        if request.POST.get('paid') == 'paid':
            paid = True

        pending = False
        if request.POST.get('pending') == 'on':
            pending = True

        description = None
        if request.POST.get('message'):
            description = request.POST.get('message')

        if request.POST.get('licence'):
            licence = request.POST.get('licence')
            try:
                driver = DriverProfile.objects.get(licence_num=licence)
                car_crime = CarCrime.objects.create(
                    stuff = request.user.staffprofile,
                    driver = driver,
                    car = car,
                    crime = crime,
                    location = location,
                    province = request.user.staffprofile.work_place.province,
                    description = description,
                    paid = paid, 
                    price = price,
                    pending = pending,
                    expiry_date = date.today() + timedelta(days=60)
                )
                if request.POST.get('paid') == 'paid':
                    payment = Payment.objects.create(
                        staff = request.user.staffprofile,
                        driver = driver,
                        owner = car.owner,
                        price = price
                    )
                    
                car_crime.payment = payment
                car_crime.save()
            except: 
                messages.info(request, 'راننده در سیستم ثبت نیست')
            return redirect('dashboard')
        else:
            car_crime = CarCrime.objects.create(
                    stuff = request.user.staffprofile,
                    car = car,
                    crime = crime,
                    location = location,
                    province = request.user.staffprofile.work_place.province,
                    description = description,
                    paid = paid, 
                    price = price,
                    pending = pending,
                    expiry_date = date.today() + timedelta(days=60)
                )
            if request.POST.get('paid') == 'paid':
                payment = Payment.objects.create(
                    staff = request.user.staffprofile,
                    owner = car.owner,
                    price = price
                )
                car_crime.payment = payment
                car_crime.save()
            return redirect('dashboard')

        
        
    
    
    context = {
        'crime_list': crime_list,
    }
    return render(request, 'crimes/create_driver_crime.html', context)

def log_payment(request, pk):
    # driver = DriverProfile.objects.get(id=pk)
    car = Car.objects.get(id=pk)
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
        owner = car.owner,
        price = total,
    )
    log.save()

    for item in car_crimes:
        item.payment = log
        item.save()
    
    return redirect('cars:car-detail', car.id)
