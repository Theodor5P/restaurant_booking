from django.urls import path
from django.http import HttpResponse

def booking_list(request):
    return HttpResponse("Booking List Page")

def create_booking(request):
    return HttpResponse("Create Booking Page")

def booking_detail(request, booking_id):
    return HttpResponse(f"Booking Detail Page - ID: {booking_id}")

def cancel_booking(request, booking_id):
    return HttpResponse(f"Cancel Booking Page - ID: {booking_id}")

app_name = 'bookings'

urlpatterns = [
    path('', booking_list, name='booking_list'),
    path('create/', create_booking, name='create_booking'),
    path('<int:booking_id>/', booking_detail, name='booking_detail'),
    path('<int:booking_id>/cancel/', cancel_booking, name='cancel_booking'),
] 