from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='car-list'),
    path('create_car/', views.create_car, name='create-car'),
    path('car_detail/<int:pk>/', views.car_detail, name='car-detail'),
    path('car_edit/<int:pk>/', views.edit_car, name = 'edit-car'),
    path('car_delete/<int:pk>/', views.delete_car, name='delete-car'),
    path('create_owner/', views.create_owner, name='create-owner'),
    path('update_owner/<int:pk>/', views.update_owner, name='update-owner'),
    path('owner_list/', views.owner_list, name='owner-list'),
    path('owner_detail/<int:pk>/', views.owner_detail, name='owner-detail'),
]
