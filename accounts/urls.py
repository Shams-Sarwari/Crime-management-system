from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.home, name='home'),
    path('driver_list/', views.driver_list, name='driver-list'),
    path('driver/<uuid:pk>/', views.driver_detail, name='driver-detail'),
    path('staff_list/', views.staff_list, name='staff-list'),
    path('staff/<uuid:pk>/', views.staff_detail, name='staff-detail'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register_driver/', views.register_driver, name='register-driver'),
    path('edit_driver_profile/<uuid:pk>/', views.edit_driver_profile, name='edit-driver-profile'),
    path('create_staff/', views.create_staff_user, name='create-staff-user'),
    path('edit_staff_profile/<uuid:pk>/', views.edit_staff_profile, name='edit-staff-profile'),
    path('delete_driver_profile/<uuid:pk>/', views.delete_driver_profile, name='delete-driver-profile'),
    path('delete_staff_profile/<uuid:pk>/', views.delete_staff_profile, name='delete-staff-profile'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'), 
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('password_reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)