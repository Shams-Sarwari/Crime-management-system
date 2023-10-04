from django.urls import path
from . import views

app_name = 'crimes'

urlpatterns = [
    path('create/', views.create_crime, name='create-crime'),
    path('crime-list/', views.crime_list, name='crime-list'),
    path('edit-crime/<int:pk>/', views.update_crime, name='edit-crime'),
    path('delete-crime/<int:pk>/', views.delete_crime, name='delete-crime'),

]
