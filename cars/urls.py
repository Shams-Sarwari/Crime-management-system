from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='car-list'),
    path('create_car/', views.create_car, name='create-car'),
    path('create_car/<int:pk>/', views.create_car, name='create-car-with-owner'),
    path('car_detail/<int:pk>/', views.car_detail, name='car-detail'),
    path('car_edit/<int:pk>/', views.edit_car, name = 'edit-car'),
    path('car_delete/<int:pk>/', views.delete_car, name='delete-car'),
    path('create_owner/', views.create_owner, name='create-owner'),
    path('update_owner/<int:pk>/', views.update_owner, name='update-owner'),
    path('owner_list/', views.owner_list, name='owner-list'),
    path('owner_detail/<int:pk>/', views.owner_detail, name='owner-detail'),
    path('delete_owner/<int:pk>/', views.delete_owner, name='delete-owner'),
    path('create_jawaz/<int:pk>/', views.create_jawaz, name='create-jawaz'),
    path('update_jawaz/<uuid:pk>/', views.update_jawaz, name='update-jawaz'), 
    path('jawaz_list/', views.jawaz_list, name='jawaz-list'),
    path('jawaz_detail/<uuid:pk>/', views.jawaz_detail, name='jawaz-detail'),
    path('delete_jawaz/<uuid:pk>/', views.delete_jawaz, name='delete-jawaz'),
]
