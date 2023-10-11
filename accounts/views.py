from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import DriverProfile, StaffProfile, User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from .forms import CustomDriverUserCreationForm, DriverEditForm, AddressForm, CustomStaffCreationForm, StaffEditForm, WorkPlaceForm, CustomPasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
# imports for custom password reset:
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from twilio.rest import Client
from django.core.mail import send_mail
from .utils import pagination_items

# Create your views here.
def home(request):
    return render(request, 'home.html')


def driver_list(request):
    drivers = DriverProfile.objects.all()
    custom_range, drivers = pagination_items(request, drivers, 5)
    context = {
        'drivers': drivers,
        'custom_range': custom_range, 
    }
    return render(request, 'accounts/driver_list.html', context)


def driver_detail(request, pk):
    driver = get_object_or_404(DriverProfile, id=pk)
    context = {
        'driver': driver
    }
    return render(request, 'accounts/driver_detail.html', context)

def staff_list(request):
    staff_list = StaffProfile.objects.all()
    custom_range, staff_list = pagination_items(request, staff_list, 10)
    context = {
        'staff_list': staff_list,
        'custom_range': custom_range,
    }
    return render(request, 'accounts/staff_list.html', context)

def staff_detail(request, pk):
    staff = get_object_or_404(StaffProfile, id=pk)
    context = {
        'staff': staff,
    }
    return render(request, 'accounts/staff_detail.html', context)

def login_user(request):
    noexist_message = None
    wrong_message = None
    check_user = None

    if request.user.is_authenticated:
        return redirect('driver_list')

    if request.method == 'POST':
        if request.POST['type'] == 'driver':

            licence_or_email = request.POST['license_or_email']
            password = request.POST['password']

            try:
                driver = DriverProfile.objects.get(licence_num = licence_or_email)
                
            except:
                noexist_message = 'Username does not exist'
                
                return render(request, 'accounts/login.html', {
                    'noexist_message': noexist_message,
                })
               
            check_user = authenticate(request, username=licence_or_email, password=password)

            if check_user is not None:
                login(request, check_user)
                return redirect('home')
                
            else: 
                wrong_message = 'Username or password is incorrect'
        
        elif request.POST['type'] == 'staff':

            licence_or_email = request.POST['license_or_email']
            password = request.POST['password']

            try:
                staff = get_user_model().objects.get(email = licence_or_email)
            except:    
                noexist_message = 'User does not exist'
                return render(request, 'accounts/login.html', {
                    'noexist_message': noexist_message,
                })           
            check_user = authenticate(request, username=licence_or_email, password=password)
            
            if check_user is not None:
                login(request, check_user)
                messages.success(request, 'You are logged in')
                return redirect('home')
            else: 
                wrong_message = 'Username or password is incorrect'


    context = {
        'noexist_message': noexist_message,
        'wrong_message': wrong_message,
    }
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')



def register_driver(request):
    
    if request.method == 'POST':
        form = CustomDriverUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_driver = True
            user.save()
            driver = DriverProfile.objects.get(user=user)
            return redirect('edit-driver-profile', driver.id)

            
    else:
        form = CustomDriverUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register_driver.html', context)


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
    }
    return render(request, 'accounts/edit_driver_profile.html', context)


def create_staff_user(request):

    if request.method == 'POST':
        form = CustomStaffCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_staff = True
            user.save()
            staff = StaffProfile.objects.get(user=user)
            return redirect('edit-staff-profile', staff.id)
    
    else: 
        form = CustomStaffCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/create_staff_user.html', context)

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
        form = StaffEditForm(request.POST, request.FILES, instance=profile)
        add_form = AddressForm(request.POST)
        work_form = WorkPlaceForm(request.POST)
        if form.is_valid() and add_form.is_valid() and work_form.is_valid():
            address = add_form.save()
            work_place = work_form.save()

            profile = form.save(commit=False)
            profile.current_address = address
            profile.work_place = work_place
            profile.save()
            return redirect('staff-detail', profile.id)


    context = {
        'form': form, 
        'add_form': add_form,
        'work_place_form': work_form,
    }
    return render(request, 'accounts/edit_staff_profile.html', context)

def delete_driver_profile(request, pk):
    profile = DriverProfile.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('driver-list')

    context = {
        'profile': profile,
    }
    return render(request, 'accounts/delete_driver_profile.html', context)

def delete_staff_profile(request, pk):
    profile = StaffProfile.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('staff-list')

    context = {
        'profile': profile,
    }
    return render(request, 'accounts/delete_staff_profile.html', context)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    
    def form_valid(self, form):
        email_or_licence = form.cleaned_data['email_or_licence']
        user = User.objects.filter(Q(email=email_or_licence) | Q(licence_num=email_or_licence)).first()

        if user:
            # generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            # Send password reset link
            reset_url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = self.request.build_absolute_uri(reset_url)

            if user.is_driver:
                account_sid = 'AC11dd7aa2c922d4e3e4e72c3e48169fbb'
                auth_token = 'f0f1895b25bce73792f22d93861c0f0f'
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                     body=f'کاربر گرامی {user.username} \n شما بخاطر درخواست تغییر رمز عبور در وبسایت ترافیک این پیام را دریافت کردید. لطفا لینک زیر را برای ادامه تنظیمات دنبال کنید. \n {reset_url}',
                     from_='+13088729493',
                     to='+93776423768'
                 )
            
            elif user.is_staff or user.is_superuser:
                user_email = user.email
                message = f'شما برای بازیابی رمز عبور خود در وبسایت رسمی ریاست ترافیک این پیام را دریافت میکنید. برای بازیابی رمز خو لینک زیر را دنبال کنید. \n {reset_url}'
                email = user.email
                send_mail('بازیابی رمز عبوز', message, 'traffic@gmail.com', [email],fail_silently=False)

        return super().form_valid(form)
        
            

