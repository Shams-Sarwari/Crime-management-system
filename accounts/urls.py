from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('driver_list/', views.driver_list, name='driver-list'),
    path('driver/<uuid:pk>/', views.driver_detail, name='driver-detail'),
    path('staff_list/', views.staff_list, name='staff-list'),
    path('staff/<uuid:pk>/', views.staff_detail, name='staff-detail'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register_driver/', views.register_driver, name='register-driver'),
    path('edit_driver_profile/<uuid:pk>/', views.edit_driver_profile, name='edit-driver-profile')
]
