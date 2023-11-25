from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateCrimeForm, CreateCarCrimeForm, ContactForm
from .models import Crime, CarCrime, Payment, Contact
from accounts.models import DriverProfile
from cars.models import Car
from accounts.models import StaffProfile
from django.contrib import messages
from datetime import date, timedelta
from django.db.models import Q
from accounts.utils import pagination_items
from django.conf import settings

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
    if request.method == 'POST':
        title = request.POST.get('title')
        min = request.POST.get('min')
        max = request.POST.get('max')
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
        return redirect('crimes:crime-list')

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
            print(f'im inside creating cirme without licence and pending is {pending}')

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
    
    return redirect('cars:car-detail', car.id)

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

def mark_contact_read(request, pk):
    if request.method == 'POST' and request.POST.get('checked') == 'checked':
        contact = Contact.objects.get(id=pk)
        contact.read = True
        contact.save()
        return redirect('crimes:notifications')
    else:
        return redirect('crimes:notifications')

def jawaz_crime_list(request):
    jawaz_crimes = CarCrime.objects.filter(
        Q(paid=False) &
        Q(crime__title='گذشتن تاریخ اعتبار جواز سیر')
    )
    custom_range, jawaz_crimes = pagination_items(request, jawaz_crimes, 6)
    context = {
        'jawaz_crimes': jawaz_crimes,
        'custom_range': custom_range,
        'section': 'jawaz'
    }
    return render(request, 'crimes/jawaz_crime_list.html', context)


# strip: 

# def calculate_order_amount(items):
#     # Replace this constant with a calculation of the order's amount
#     # Calculate the order total on the server to prevent
#     # people from directly manipulating the amount on the client
#     return 1400

# @csrf_exempt
# @require_POST
# def create_payment(request):
#         print('this view called')
#         print(request.POST)
#     # loop over the values of the sent data and find the crimes
#     # if request.method == 'POST':
#         try:
#             print('start try')
#             num_of_crimes = int(request.POST.get('num_of_crimes'))
#             for i in range(1, num_of_crimes+1):
#                 crime_ids.append(request.POST.get(i))
#             print('inside try')
#         except:
#             pass
#         crime_ids = []
        

#         try:
#             data = json.loads(request.body)
#             # Create a PaymentIntent with the order amount and currency
#             intent = stripe.PaymentIntent.create(
#                 amount=calculate_order_amount(data['items']),
#                 currency='usd',
#                 automatic_payment_methods={
#                     'enabled': True,
#                 },
#             )

#             # if everything is ok:
#             for item in crime_ids:
#                 crime = get_object_or_404(CarCrime, id=item)
#                 crime.paid = True
#                 crime.save()

#             return JsonResponse({
#                 'clientSecret': intent['client_secret']
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=403)
        

def success_view(request):
    return render(request, 'crimes/success.html')

def cancel_view(request):
    return render(request, 'crimes/cancel.html')


@csrf_exempt
def strip_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    

@csrf_exempt
def create_checkout_session(request, crimes):
    crimes = crimes.rstrip(',')
    crime_ids = crimes.split(',')
    print(crime_ids)    
    
    total_price = 0
    for item in crime_ids:
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
                
                success_url= domain_url + 'success/',
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
            log = Payment.objects.create(
                price = total_price,
                online = True,  
            )
            for item in crime_ids:
                crime = get_object_or_404(CarCrime, id=int(item))
                crime.paid = True
                crime.payment = log
                crime.save()
            
            

                    
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})