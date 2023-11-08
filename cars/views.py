from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, CarOwner, CarHistory, JawazSayr, OldHistory
from crimes.models import CarCrime, Crime
from .forms import CreateCarForm, EditCarForm, CreateOwnerForm, JawazForm
from django.http import HttpResponse
from accounts.models import DriverProfile
from accounts.utils import pagination_items
from django.db.models import Q
from datetime import date, timedelta
from django.contrib import messages
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
    crimes = car.carcrime_set.filter(
        Q(paid=False) &
        Q(pending=False)
        )
    
    # check if the jawazsayr expiry date is passed. if so fine the driver
    try:
        jawaz_sayr = JawazSayr.objects.get(car=car)
    except:
        jawaz_sayr = None
    
    if jawaz_sayr:
        while jawaz_sayr.expiry_date < date.today():
            if date.today() > jawaz_sayr.expiry_date:
                    crime = CarCrime.objects.create(
                        car = car,
                        crime = Crime.objects.get(title='گذشتن تاریخ اعتبار جواز سیر'),
                        price = 500, 
                        expiry_date = jawaz_sayr.expiry_date + timedelta(days=60)

                    )
                    crime.save()
                    jawaz_sayr.expiry_date += timedelta(days=90)
                    jawaz_sayr.save()
                    
    for item in crimes:
        while item.expiry_date < date.today() and item.paid == False and crime.pending == False:
            if (date.today() > item.expiry_date) and (item.paid == False) and (crime.pending == False):
                item.expiry_fine += item.price/2
                item.expiry_date += timedelta(days=60)
                item.save()

    context = {
        'car': car, 
        'history': car_history,
        'crimes': crimes,
        'section': 'cars'
    }
    return render(request, 'cars/car_detail.html', context)

def create_car(request, pk=None):
    
    if request.method == 'POST':
        form = CreateCarForm(request.POST)
        if form.is_valid():
            if pk:
                owner = CarOwner.objects.get(id=pk)
                car = form.save(commit=False)
                car.owner = owner
                car.save()
                return redirect('cars:owner-detail', owner.id)
            
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
    
    car_owner = car.owner
    new_owner = None
    

    
    if request.method=='POST':
        
        # create a history if driver or owner has been updated
        if request.POST['owner_tazkira'] != '':
            try: 
                new_owner = CarOwner.objects.get(tazkira_number = request.POST['owner_tazkira'])
            except:
                messages.error(request, 'مالک با این مشخضات در سیستم وجود ندارد')
                return redirect('cars:car-detail', car.id)
            
            if car_owner != new_owner:
                owner_history = CarHistory.objects.create(
                    car = car, 
                    owner = new_owner
                )
                owner_history.save()
                OldHistory.objects.create(
                    car_history = owner_history, 
                    old_owner = car_owner,
                )


                car.owner = new_owner
                car.save()
        if request.POST['plate_num'] != '':
            plates = Car.objects.values_list('plate_number', flat=True)
            if request.POST['plate_num'] in plates:
                messages.error(request, 'این پلیت نمبر در موتر دیگری ثبت است')
                return redirect('cars:car-detail', car.id)
            car.plate_number = request.POST['plate_num']
            car.save()
            
        
        messages.success(request, 'تغییرات با موفقیت اعمال شد')
        
    return redirect('cars:car-detail', car.id)
    

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
    cars = owner.car_set.all()
    
    try:
        jawaz_sayr = JawazSayr.objects.filter(car__owner=owner)
    except:
        jawaz_sayr = None
    
    
    if jawaz_sayr:
        for item in jawaz_sayr:
            while item.expiry_date < date.today():
                if date.today() > item.expiry_date:
                    crime = CarCrime.objects.create(
                        car = item.car,
                        crime = Crime.objects.get(title='گذشتن تاریخ اعتبار جواز سیر'),
                        price = 500, 
                        expiry_date = item.expiry_date + timedelta(days=60)

                    )
                    crime.save()
                    item.expiry_date += timedelta(days=90)
                    item.save()
    
    for car in cars:
        for crime in car.carcrime_set.all():
            while crime.expiry_date < date.today() and crime.paid == False and crime.pending == False:
                if (date.today() > crime.expiry_date) and (crime.paid == False) and (crime.pending == False):
                    crime.expiry_fine += crime.price/2
                    crime.expiry_date += timedelta(days=60)
                    crime.save()
        

    context = {
        'owner': owner, 
        'section': 'owners',
        'num_of_cars': cars.count(),
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
    
    driver = car.driver
    if driver == None: 
        messages.info(request, 'لطفا ابتدا برای این موتر راننده اضافه کنید')
        return redirect('cars:car-detail', car.id)
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

def delete_jawaz(request, pk):
    jawaz = get_object_or_404(JawazSayr, id=pk)
    car = jawaz.car
    if request.method == 'POST':
        jawaz.delete()
    
    return redirect('cars:car-detail', car.id)