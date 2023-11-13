from django.http import HttpResponse
from django.shortcuts import redirect

def superuser_or_staff_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("معذرت میخواهیم شما اجازه دسترسی به این صفحه را ندارید")
    return wrapper_func

def superuser_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("معذرت میخواهیم شما اجازه دسترسی به این صفحه را ندارید")
    return wrapper_func