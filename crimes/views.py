from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateCrimeForm, CreateCarCrimeForm, ContactForm
from .models import Crime, CarCrime, Payment, Contact
from accounts.models import DriverProfile
from cars.models import Car, CarOwner
from accounts.models import StaffProfile
from django.contrib import messages
from datetime import date, timedelta
from django.db.models import Q
from accounts.utils import pagination_items
from django.urls import reverse_lazy
from django.conf import settings
from twilio.rest import Client
# strip imports:
import json
import stripe

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import superuser_or_staff_required, superuser_required


# stripe.api_key = 'sk_test_51OAQ0PItY091qK4GuGeFsuNbfSdGYcMuoHMnFysmYi4WQbPkf2CfGxKHcB1wyuDUedNBPORVjMM7PMVxQa2IQ2yG00dSLua5iU'

# Create your views here.
@login_required(login_url='login')
@superuser_required
def create_crime(request):
    crimes = Crime.objects.all()
    custom_range, crimes = pagination_items(request, crimes, 6)

    if request.method == 'POST':
        title = request.POST.get('title')
        min = float(request.POST.get('min'))
        if request.POST.get('max'):
            max = float(request.POST.get('max'))
        else:
            max = None
        desc = request.POST.get('description')
        Crime.objects.create(
            title = title, 
            description = desc, 
            min_price = min,
            max_price = max, 
        )
        messages.success(request, 'موضوع جریمه موفقانه ثبت سیستم گردید')
        return redirect('crimes:create-crime')
    else:
        form = CreateCrimeForm()

    context = {
        'form': form,
        'crimes': crimes,
        'custom_range': custom_range,
        'section': 'crime_subject'
    }
    return render(request, 'crimes/create_crime.html', context)

@login_required(login_url='login')
@superuser_required
def crime_list(request):
    crimes = Crime.objects.all()
    context = {
        'crimes': crimes
    }
    return render(request, 'crimes/crime_list.html', context)

@login_required(login_url='login')
@superuser_required
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

@login_required(login_url='login')
@superuser_required
def delete_crime(request, pk):
    crime = Crime.objects.get(id=pk)
    if request.method == 'POST':
        crime.delete()
        messages.success(request, 'موضوع موفقانه از سیستم حذف گردید')
        return redirect('crimes:create-crime')

    context = {
        'crime': crime
    }
    return render(request, 'crimes/delete_crime.html', context)

@login_required(login_url='login')
@superuser_or_staff_required
def driver_crime_list(request):
    crimes = CarCrime.objects.all()
    context = {
        'crimes': crimes
    }
    return render(request, 'crimes/driver_crime_list.html', context)

@login_required(login_url='login')
@superuser_or_staff_required
def create_car_crime(request):
    profile = StaffProfile.objects.get(user = request.user)
    all_crimes = Crime.objects.all().exclude(title='گذشتن تاریخ اعتبار جواز سیر')
    crime_list = []
    for item in all_crimes:
        temp = []
        temp.append(item.title)
        temp.append(str(int(item.min_price)))
        if item.max_price:
            temp.append(str(int(item.max_price)))
        else:
            temp.append('')
        crime_list.append(temp)
    
    

    
    if request.method == 'POST':
        plate = request.POST.get('plate')
        try:
            car = Car.objects.get(plate_number=plate)
            
        except:
            messages.error(request, 'پلیت نمبر وارد شده در سیستم موجود نیست')
            return redirect('crimes:fine-driver')
        crime = None
        if request.POST.get('crime_type'):
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
        if request.POST.get('pending') == 'pending':
            pending = True

        description = None
        if request.POST.get('message'):
            description = request.POST.get('message')

        if request.POST.get('licence'):
            licence = request.POST.get('licence')
            if car.owner.licence_number == licence:
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
                # generate a message to driver's phone number:
                # payment_url = reverse_lazy('cars:owner-detail', kwargs={'pk':car.owner.id})
                # payment_url = request.build_absolute_uri(payment_url)
                # account_sid = 'AC107249e5f7742024a4dfc4c9bc091350'
                # auth_token = '6f1f266ae8955e4ca0ac895698549f2a'
                # client = Client(account_sid, auth_token)
                # message = client.messages.create(
                #     body= f'\u202Eکاربر گرامی، شما بخاطر نقض قوانین ترافیکی ({crime.title}) از طرف ریاست ترافیک، مبلغ ({price}) افغانی جریمه شدید لطفا برای پرداخت نمودن جریمه خود به لینک زیر مراجعه نمایید \n {payment_url}',
                #     from_='+14842287089',
                #     to='+93793545428'
                # )
                # print(message.sid)

                if request.POST.get('paid') == 'paid':
                    payment = Payment.objects.create(
                        staff = request.user.staffprofile,
                        owner = car.owner,
                        price = price
                    )
                    car_crime.payment = payment
                    car_crime.save()
                return redirect('cars:owner-detail', car.owner.id)
            try:
                driver = DriverProfile.objects.get(licence_num=licence)
            except: 
                messages.info(request, 'راننده در سیستم ثبت نیست')
                return redirect('crimes:fine-driver')
                
            else:
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
                
                # generate a message to driver's phone number:
                # payment_url = reverse_lazy('cars:owner-detail', kwargs={'pk':car.owner.id})
                # payment_url = request.build_absolute_uri(payment_url)

                # account_sid = 'AC107249e5f7742024a4dfc4c9bc091350'
                # auth_token = '6f1f266ae8955e4ca0ac895698549f2a'
                # client = Client(account_sid, auth_token)
                # message = client.messages.create(
                #     body= f'\u202Eکاربر گرامی، شما بخاطر نقض قوانین ترافیکی ({crime.title}) از طرف ریاست ترافیک، مبلغ ({price}) افغانی جریمه شدید لطفا برای پرداخت نمودن جریمه خود به لینک زیر مراجعه نمایید \n {payment_url}',
                #     from_='+14842287089',
                #     to='+93793545428'
                # )
                # print(message.sid)

                if request.POST.get('paid') == 'paid':
                    payment = Payment.objects.create(
                        staff = request.user.staffprofile,
                        driver = driver,
                        owner = car.owner,
                        price = price
                    )
                        
                    car_crime.payment = payment
                    car_crime.save()
                return redirect('cars:owner-detail', car.owner.id)
                
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
            
            # generate a message to driver's phone number:
            # payment_url = reverse_lazy('cars:owner-detail', kwargs={'pk':car.owner.id})
            # payment_url = request.build_absolute_uri(payment_url)

            # account_sid = 'AC107249e5f7742024a4dfc4c9bc091350'
            # auth_token = '6f1f266ae8955e4ca0ac895698549f2a'
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     body= f'\u202Eکاربر گرامی، شما بخاطر نقض قوانین ترافیکی ({crime.title}) از طرف ریاست ترافیک، مبلغ ({price}) افغانی جریمه شدید لطفا برای پرداخت نمودن جریمه خود به لینک زیر مراجعه نمایید \n {payment_url}',
            #     from_='+14842287089',
            #     to='+93793545428'
            # )
            # print(message.sid)

            if request.POST.get('paid') == 'paid':
                payment = Payment.objects.create(
                    staff = request.user.staffprofile,
                    owner = car.owner,
                    price = price
                )
                car_crime.payment = payment
                car_crime.save()
            
            return redirect('cars:owner-detail', car.owner.id)
            

        
        
    
    
    context = {
        'crime_list': crime_list,
        'section': 'crime',
    }
    return render(request, 'crimes/create_driver_crime.html', context)

@login_required(login_url='login')
@superuser_or_staff_required
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
    
    return redirect('cars:success-payment', log.id)

@login_required(login_url='login')
@superuser_required
def notification(request):
    pending_crimes = CarCrime.objects.filter(
        Q(pending=True) &
        Q(province=request.user.staffprofile.work_place.province)
        )
    num_of_pending_crimes = pending_crimes.count()

    pending_comments = Contact.objects.filter(read=False)
    num_of_pending_comments = pending_comments.count()
    context = {
        'pending_crimes': pending_crimes,
        'num_of_pending_crimes': num_of_pending_crimes,
        'pending_comments': pending_comments, 
        'num_of_pending_comments': num_of_pending_comments,
    }
    return render(request, 'crimes/notifications.html', context)

@login_required(login_url='login')
@superuser_required
def remove_pending(request, pk):
    crime = get_object_or_404(CarCrime, id=pk)
    if request.method == 'POST':
        price = request.POST.get('price')
        crime.price = price
        crime.pending = False
        crime.save()
    return redirect('crimes:notifications')


def online_payment(request):
    
    total = 0
    if request.method == 'POST':    
        car_crimes = []
        paid_crimes = request.POST.getlist('paid_crimes')
        
        for i in paid_crimes:
            crime = CarCrime.objects.get(id=int(i))
            car_crimes.append(crime)
            total += crime.price + crime.expiry_fine
            # crime.paid = True
            # crime.save()
            # car_crimes.append(crime)
        
        print(car_crimes)
        print(len(car_crimes))
            
    context = {
        'total': total,
        'paid_crimes': car_crimes, 
        'num_of_crimes': len(paid_crimes),
    }
    return render(request, 'crimes/checkout.html', context)


def create_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        Contact.objects.create(
            name = name,
            email = email, 
            comment = comment, 

        )
        
        messages.success(request, 'نظر شما موفقانه ثبت گردید.')
        return redirect('home')

@login_required(login_url='login')
@superuser_required
def mark_contact_read(request, pk):
    if request.method == 'POST' and request.POST.get('checked') == 'checked':
        contact = Contact.objects.get(id=pk)
        contact.read = True
        contact.save()
        return redirect('crimes:notifications')
    else:
        return redirect('crimes:notifications')

@login_required(login_url='login')
@superuser_required
def jawaz_crime_list(request):
    jawaz_crimes = CarCrime.objects.filter(
        Q(paid=False) &
        Q(crime__title='گذشتن تاریخ اعتبار جواز سیر')
    )
    
    # do caching to bring jawaz crimes with related dependencies
    jawaz_crimes = jawaz_crimes.select_related('car')

    custom_range, jawaz_crimes = pagination_items(request, jawaz_crimes, 8)
    context = {
        'jawaz_crimes': jawaz_crimes,
        'custom_range': custom_range,
        'section': 'jawaz'
    }
    return render(request, 'crimes/jawaz_crime_list.html', context)



def success_view(request, crimes):
    crimes = crimes.rstrip(',')
    crime_ids = crimes.split(',')
    status = crime_ids[0]
    status_id = crime_ids[1]
    owner = None
    driver = None
    if status == 'owner': 
        owner = get_object_or_404(CarOwner, id=int(status_id))
    elif status == 'driver': 
        driver = get_object_or_404(DriverProfile, id=status_id)
    
    total_price = 0
    for item in crime_ids[2:]:
        crime = get_object_or_404(CarCrime, id=int(item))
        total_price += crime.price
        total_price += crime.expiry_fine
    
    if owner:
        log = Payment.objects.create(
            price = total_price,
            owner = owner,
            online = True,  
        )
    elif driver:
        log = Payment.objects.create(
            price = total_price,
            driver = driver,
            online = True,  
        )
    for item in crime_ids[2:]:
        crime = get_object_or_404(CarCrime, id=int(item))
        crime.paid = True
        crime.payment = log
        crime.save()
            
    context = {
        'payment': log
    }
    return render(request, 'cars/success_payment.html', context)

def cancel_view(request):
    return render(request, 'crimes/cancel.html')


@csrf_exempt
def strip_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    

@csrf_exempt
def create_checkout_session(request, crimes):
    print(crimes)
    crimes = crimes.rstrip(',')
    crime_ids = crimes.split(',')
    
    
    
    total_price = 0
    for item in crime_ids[2:]:
        crime = get_object_or_404(CarCrime, id=int(item))
        total_price += crime.price
        total_price += crime.expiry_fine
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
          
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            
            checkout_session = stripe.checkout.Session.create(
                # success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                
                success_url= domain_url + 'success/' + crimes,
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                {
                    'price_data': {
                        'currency': 'afn',
                        'unit_amount': str(int(total_price * 100)),
                        'product_data': {
                            'name': 'Payment of crimes'
                        },
                    },
                    'quantity': 1,
                },
            ]
            )
            
            

                    
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        

@login_required(login_url='login')
@superuser_required
def payment_list(request):
    search_id = None
    payments = Payment.objects.all().order_by('-id')
    years_of_payments = Payment.objects.values_list('created__year', flat=True).distinct()
    
    # also bring dependencies in cache
    payments = payments.select_related('staff', 'driver', 'owner')
    custom_range, payments = pagination_items(request, payments, 7)



    if request.method == "POST" and request.POST.get('search_id'):
        search_id = int(request.POST.get('search_id'))
        print(search_id)
        try:
            payments = Payment.objects.filter(id=search_id)
        except:
            payments = []
        
    

    context = {
        'payments': payments,
        'years': years_of_payments,
        'num_of_payments': len(payments),
        'custom_range': custom_range,
        'search_id': search_id,
        'section': 'payment'
    }
    return render(request, 'crimes/payment_list.html', context)