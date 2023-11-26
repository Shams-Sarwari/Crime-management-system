"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from crimes.views import create_checkout_session, strip_config, success_view, cancel_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cars/', include('cars.urls')),
    path('crime/', include('crimes.urls')),
    # stripe urls
    path('create-checkout-session/<str:crimes>/', create_checkout_session, name="create-checkout-session"),
    path('strip-config/', strip_config, name='stripe-config'),
    path('success/<str:crimes>/', success_view, name='success'),
    path('cancelled/', cancel_view, name='cancelled'),

    
    path('', include('accounts.urls')),
    
]
