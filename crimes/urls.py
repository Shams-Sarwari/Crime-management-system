from django.urls import path
from . import views

app_name = 'crimes'

urlpatterns = [
    path('create/', views.create_crime, name='create-crime'),

]
