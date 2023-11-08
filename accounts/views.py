from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import DriverProfile, StaffProfile, User, WorkPlace
from cars.models import JawazSayr, CarOwner
from crimes.models import CarCrime,Crime, Payment
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from .forms import CustomDriverUserCreationForm, DriverEditForm, AddressForm, CustomStaffCreationForm, StaffEditForm, WorkPlaceForm, CustomPasswordResetForm, CustomPasswordChangeForm, CustomSetPasswordForm, OwnerEditForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.contrib import messages
# imports for custom password reset:
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from twilio.rest import Client
from django.core.mail import send_mail
from .utils import pagination_items
from django.contrib import messages
from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models.functions import ExtractYear, ExtractMonth


# Create your views here.
@login_required(login_url='login')
def dashboard(request, city='کابل', year=datetime.now().year):
    # offline payments section:
    offline_payments = CarCrime.objects.filter(payment__created=date.today())
    offline_total_price = 0
    for item in offline_payments:
        offline_total_price += item.price + item.expiry_fine

    
    # online payment section:

    # number of todays crime:
    current_date = timezone.now().date()
    start_of_day = datetime.combine(current_date, datetime.min.time())
    end_of_day = datetime.combine(current_date, datetime.max.time())
    today_crimes_list = CarCrime.objects.filter(created__range=(start_of_day, end_of_day))
    today_crimes = len(today_crimes_list)

    # monthly payment:
    monthly_total = 0
    current_year = timezone.now().year
    current_month = timezone.now().month
    start_of_month = timezone.datetime(current_year, current_month, 1).date()
    try:
        end_of_month = start_of_month.replace(day=31)
    except:
        try:
            end_of_month = start_of_month.replace(day=30)
        except:
            try:
                end_of_month = start_of_month.replace(day=29)
            except:
                end_of_month = start_of_month.replace(day=28)

    payments_of_this_month = Payment.objects.filter(created__range=(start_of_month, end_of_month))
    for item in payments_of_this_month:
        monthly_total += item.price

    # send provinces that this system is available for them to template
    provinces = CarCrime.objects.distinct().exclude(province=None).values_list('province', flat=True)
    
    # send years of crimes which are in database
    years = CarCrime.objects.distinct().annotate(year=ExtractYear('created')).values_list('year', flat=True)
    
    # send data to circular graph
    province_crime_dict = {}
    for province in provinces:
        province_crime_dict[province]=len(CarCrime.objects.filter(province=province, created__year=datetime.now().year))

    sorted_province_dict = dict(sorted(province_crime_dict.items(), key=lambda x: x[1], reverse=True))
    

    i = len(sorted_province_dict)
    if i >= 3:
        i = 3
    j = 0
    top_three_provinces = []
    top_three_values = []
    for key, value in sorted_province_dict.items():
        if j < i:
            top_three_provinces.append(key)
            top_three_values.append(value)
            j += 1
        else:
            break
    
    # send data to main graph
    filter_province = None
    filter_year = None

    if request.method == 'POST':
        if request.POST.get('selected_province'):
            city = request.POST.get('selected_province')
            filter_province = city
        if request.POST.get('selected_year'):
            year = request.POST.get('selected_year')
            filter_year = year

    crimes_in_months = []
    for i in range(1, 13):  
        crimes_in_months.append(CarCrime.objects.filter(
            Q(province=city) &
            Q(created__year=year) &
            Q(created__month=i) 
            ).count())
    
    
    
        
        
    
    

    context = {
        'section': 'dashboard',
        'offline_total_price': offline_total_price,
        'today_crimes': today_crimes,
        'monthly_total': monthly_total,
        'provinces': provinces,
        'years': years,
        'top_three_provinces': top_three_provinces,
        'top_three_values': top_three_values,
        'filter_province': filter_province,
        'filter_year': filter_year,
        'crimes_in_months': crimes_in_months,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def driver_list(request):
    search_text = ''
    if request.GET.get('search_text'):
        search_text = request.GET.get('search_text')
    drivers = DriverProfile.objects.distinct().filter(
        Q(first_name__icontains=search_text)|
        Q(licence_num=search_text) | 
        Q(tazkira_num=search_text)
    )
    custom_range, drivers = pagination_items(request, drivers, 10)
    context = {
        'drivers': drivers,
        'custom_range': custom_range, 
        'search_text': search_text,
        'section': 'drivers'
    }
    return render(request, 'accounts/driver_list.html', context)

@login_required(login_url='login')
def driver_detail(request, pk):
    driver = get_object_or_404(DriverProfile, id=pk)
    context = {
        'driver': driver,
        'section': 'drivers', 
    }
    return render(request, 'accounts/driver_detail.html', context)

@login_required(login_url='login')
def staff_list(request):
    search_text = ''
    if request.GET.get('search_text'):
        search_text = request.GET.get('search_text')

    staff_list = StaffProfile.objects.distinct().filter(
            Q(first_name__icontains=search_text)|
            Q(email=search_text) | 
            Q(tazkira_num=search_text)        
    )
    custom_range, staff_list = pagination_items(request, staff_list, 10)
    context = {
        'staff_list': staff_list,
        'custom_range': custom_range,
        'search_text': search_text,
        'section': 'staffs',
    }
    return render(request, 'accounts/staff_list.html', context)

@login_required(login_url='login')
def staff_detail(request, pk):
    staff = get_object_or_404(StaffProfile, id=pk)
    has_tazkira = False
    if staff.tazkira_img:
        has_tazkira = True
    context = {
        'staff': staff,
        'section': 'staffs',
        'has_tazkira': has_tazkira,
    }
    return render(request, 'accounts/staff_detail.html', context)

def login_user(request):
    check_user = None

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        if request.POST['type'] == 'driver':

            licence_or_email = request.POST['license_or_email']
            password = request.POST['password']

            try:
                driver = DriverProfile.objects.get(licence_num = licence_or_email)
                
            except:

                messages.error(request, 'اکانت با لایسنس نمبر وارد شده موجود نیست')

               
            check_user = authenticate(request, username=licence_or_email, password=password)

            if check_user is not None:
                login(request, check_user)
                messages.success(request, 'شما موفقانه وارد سیستم شدید')
                return redirect('dashboard')
                
            else: 

                messages.error(request, 'لایسنس نمبر یا رمز عبور وارد شده اشتباه است')

        
        elif request.POST['type'] == 'staff':

            licence_or_email = request.POST['license_or_email']
            password = request.POST['password']

            try:
                staff = get_user_model().objects.get(email = licence_or_email)

            except:    
                messages.error(request, 'ایمیل وارد شده در سیستم موجود نیست')

            check_user = authenticate(request, username=licence_or_email, password=password)
            
            if check_user is not None:
                login(request, check_user)
                messages.success(request, 'شما موفقانه وارد سیستم شدید')
                return redirect('dashboard')
            else: 

                messages.error(request, 'ایمیل و یا رمز عبور وارد شده اشتباه است')
        
        elif request.POST['type'] == 'owner':

            licence_or_email = request.POST['license_or_email']
            password = request.POST['password']

            try:
                owner = CarOwner.objects.get(tazkira_number = licence_or_email)
                
            except:

                messages.error(request, 'اکانت با تذکره نمبر وارد شده موجود نیست')

               
            check_user = authenticate(request, username=licence_or_email, password=password)

            if check_user is not None:
                login(request, check_user)
                messages.success(request, 'شما موفقانه وارد سیستم شدید')
                return redirect('dashboard')
                
            else: 

                messages.error(request, 'تذکره نمبر یا رمز عبور وارد شده اشتباه است')

  


    context = {

    }
    return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def register_driver(request):
    
    if request.method == 'POST':
        form = CustomDriverUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_driver = True
            user.save()
            driver = DriverProfile.objects.get(user=user)
            messages.success(request,'راننده با موفقیت ثبت شد.')
            return redirect('edit-driver-profile', driver.id)

            
    else:
        form = CustomDriverUserCreationForm()
    context = {
        'form': form,
        'section': 'drivers',
    }
    return render(request, 'accounts/register_driver.html', context)

@login_required(login_url='login')
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
            return redirect('driver-detail', profile.id)


    context = {
        'form': form, 
        'add_form': add_form,
        'section': 'drivers'
    }
    return render(request, 'accounts/edit_driver_profile.html', context)

def register_owner(request):
    
    if request.method == 'POST':
        form = CustomDriverUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_owner = True
            user.save()
            owner = CarOwner.objects.get(user=user)
            messages.success(request,'مالک با موفقیت ثبت شد.')
            return redirect('cars:update-owner', owner.id)

            
    else:
        form = CustomDriverUserCreationForm()
    context = {
        'form': form,
        'section': 'owners',
    }
    return render(request, 'accounts/register_owner.html', context)


    
@login_required(login_url='login')
def create_staff_user(request):

    if request.method == 'POST':
        form = CustomStaffCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_staff = True
            user.email = user.username
            user.save()
            staff = StaffProfile.objects.get(user=user)
            return redirect('edit-staff-profile', staff.id)
    
    else: 
        form = CustomStaffCreationForm()
    
    context = {
        'form': form,
        'section': 'staffs',
    }
    return render(request, 'accounts/create_staff_user.html', context)

@login_required(login_url='login')
def edit_staff_profile(request, pk):
    profile = StaffProfile.objects.get(id = pk)
    form = StaffEditForm(instance=profile)
    
    if profile.current_address is not None:
        add_form = AddressForm(instance=profile.current_address)
    else: 
        add_form = AddressForm()
    
    if profile.work_place is not None:
        work_form = WorkPlaceForm(instance=profile.work_place)
    else:
        work_form = WorkPlaceForm()

    if request.method == 'POST':
        avatar = request.FILES.get('prof_pic', None)
        form = StaffEditForm(request.POST, request.FILES, instance=profile)
        add_form = AddressForm(request.POST)
        work_form = WorkPlaceForm(request.POST)
        if form.is_valid() and add_form.is_valid() and work_form.is_valid():
            address = add_form.save()
            work_place = work_form.save()

            profile = form.save(commit=False)
            profile.current_address = address
            profile.work_place = work_place
            if avatar:
                profile.avatar = request.FILES['prof_pic']
            profile.save()
            return redirect('staff-detail', profile.id)


    context = {
        'form': form, 
        'add_form': add_form,
        'work_place_form': work_form,
        'section': 'staffs',
    }
    return render(request, 'accounts/edit_staff_profile.html', context)

@login_required(login_url='login')
def delete_driver_profile(request, pk):
    profile = DriverProfile.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'راننده با موفقیت حذف گردید')
        return redirect('driver-list')
    delete = 'true'
    context = {
        'driver': profile,
        'delete': delete, 
        'section': 'drivers',
    }
    
    return render(request, 'accounts/driver_detail.html', context)

@login_required(login_url='login')
def delete_staff_profile(request, pk):
    profile = StaffProfile.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'کارمند موفقانه حذف شد')
        return redirect('staff-list')

    delete = 'true'
    context = {
        'profile': profile,
        'delete': delete, 
        'section': 'staffs'
    }
    return render(request, 'accounts/delete_staff_profile.html', context)

@login_required(login_url='login')
def change_staff_avatar(request, pk):
    staff = StaffProfile.objects.get(id=pk)
    if request.method == 'POST' and request.FILES.get('photo'):
        image = request.FILES.get('photo')
        staff.avatar = image
        staff.save()
    messages.success(request, 'پروفایل موفقانه تبدیل گردید')
    return redirect('staff-detail', staff.id)
@login_required(login_url='login')
def change_staff_to_admin(request, pk):
    staff = StaffProfile.objects.get(id=pk)
    if request.method == 'POST' and request.POST.get('admin'):
        staff.user.is_superuser = True
        staff.user.save()
        messages.success(request, 'کارمند مذکور به ادمین تبدیل گردید')
        
    return redirect('staff-detail', staff.id)

def deactive_staff(request, pk):
    staff = StaffProfile.objects.get(id=pk)
    if request.method == 'POST' and request.POST.get('deactive'):
        staff.user.is_active = False
        staff.user.save()
        messages.success(request, 'کارمند موفقانه غیرفعال گردید')
        
    
    elif request.method == 'POST':
        staff.user.is_active = True
        staff.user.save()
        messages.success(request, 'کارمند موفقانه فعال گردید')
        
    return redirect('staff-detail', staff.id)

    return redirect


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    
    def form_valid(self, form):
        email_or_licence = form.cleaned_data['email_or_licence']
        user = User.objects.filter(Q(email=email_or_licence) | Q(username=email_or_licence)).first()

        if user:
            # generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            # Send password reset link
            reset_url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = self.request.build_absolute_uri(reset_url)

            
            account_sid = 'AC11dd7aa2c922d4e3e4e72c3e48169fbb'
            auth_token = 'f0f1895b25bce73792f22d93861c0f0f'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                    body=f'کاربر گرامی {user.username} \n شما بخاطر درخواست تغییر رمز عبور در وبسایت ترافیک این پیام را دریافت کردید. لطفا لینک زیر را برای ادامه تنظیمات دنبال کنید. \n {reset_url}',
                    from_='+13088729493',
                    to='+93776423768'
                )
        
            # elif user.is_staff or user.is_superuser:
            #     user_email = user.email
            #     message = f'شما برای بازیابی رمز عبور خود در وبسایت رسمی ریاست ترافیک این پیام را دریافت میکنید. برای بازیابی رمز خو لینک زیر را دنبال کنید. \n {reset_url}'
            #     email = user.email
            #     send_mail('بازیابی رمز عبوز', message, 'traffic@gmail.com', [email],fail_silently=False)
        
        
            

        return super().form_valid(form)


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm

            
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm

