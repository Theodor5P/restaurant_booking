from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Booking management
    path('', views.booking_list, name='booking_list'),
    path('create/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # Restaurant information
    path('restaurant-info/', views.restaurant_info, name='restaurant_info'),
    path('check-availability/', views.check_availability, name='check_availability'),
] 