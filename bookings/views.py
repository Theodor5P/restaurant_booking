from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from restaurants.models import Restaurant, TimeSlot


@login_required
def booking_list(request):
    """List user's bookings."""
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'bookings/booking_list.html', {
        'bookings': bookings
    })


@login_required
def create_booking(request):
    """Create a new booking."""
    if request.method == 'POST':
        # Booking creation logic will be implemented later
        messages.success(request, 'Booking created successfully!')
        return redirect('bookings:booking_list')
    
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, 'bookings/create_booking.html', {
        'restaurants': restaurants
    })


@login_required
def booking_detail(request, booking_id):
    """Show booking details."""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking
    })


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if booking.cancel():
        messages.success(request, 'Booking cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    
    return redirect('bookings:booking_list') 