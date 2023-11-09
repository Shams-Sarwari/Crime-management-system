from django.urls import path
from . import views

app_name = 'crimes'

urlpatterns = [
    path('create/', views.create_crime, name='create-crime'),
    path('crime-list/', views.crime_list, name='crime-list'),
    path('edit-crime/<int:pk>/', views.update_crime, name='edit-crime'),
    path('delete-crime/<int:pk>/', views.delete_crime, name='delete-crime'),
    path('driver-crime-list/', views.driver_crime_list, name='driver-crime-list'),
    path('fine-driver/', views.create_car_crime, name='fine-driver'),
    path('log-payment/<int:pk>/', views.log_payment, name='log-payment'),
    path('notifications/', views.notification, name='notifications'),
    path('remove_pending/<int:pk>/', views.remove_pending, name='remove-pending'),
    # stipe: 
    path('online_payment/', views.online_payment, name='online-payment'),
    path('create-payment-intent', views.create_payment, name='create_payment'),
    

]
