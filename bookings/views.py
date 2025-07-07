from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Booking
from .forms import BookingForm, BookingFilterForm, AvailabilityCheckForm
from restaurants.models import Restaurant, TimeSlot
from django.db import IntegrityError
from django.core.exceptions import ValidationError


def booking_list(request):
    """List all bookings with filtering options."""
    bookings = Booking.objects.all().select_related(
        'customer', 'restaurant', 'time_slot'
    ).order_by('-date', '-time_slot__time')
    
    # Apply filters
    filter_form = BookingFilterForm(request.GET)
    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        status = filter_form.cleaned_data.get('status')
        time_slot = filter_form.cleaned_data.get('time_slot')
        
        if date_from:
            bookings = bookings.filter(date__gte=date_from)
        if date_to:
            bookings = bookings.filter(date__lte=date_to)
        if status:
            bookings = bookings.filter(status=status)
        if time_slot:
            bookings = bookings.filter(time_slot=time_slot)
    
    # Pagination
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'total_bookings': bookings.count(),
    }
    
    return render(request, 'bookings/booking_list.html', context)


@login_required
def create_booking(request):
    """Create a new booking."""
    # Get the restaurant (assuming single restaurant for now)
    try:
        restaurant = Restaurant.objects.get(is_active=True)
    except Restaurant.DoesNotExist:
        messages.error(request, 'No active restaurant found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, restaurant=restaurant, instance=Booking(restaurant=restaurant))
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.restaurant = restaurant
            try:
                booking.full_clean()
                booking.save()
                messages.success(
                    request, 
                    f'Booking confirmed for {booking.date} at {booking.time_slot.time.strftime("%H:%M")}!'
                )
                return redirect('bookings:booking_detail', booking_id=booking.id)
            except (IntegrityError, ValidationError) as e:
                form.add_error(None, "A booking with this customer, restaurant, date, and time slot already exists.")
        else:
            messages.error(request, 'Booking failed. Please correct the errors.')
    else:
        # Pre-fill form with data from availability check if provided
        initial_data = {}
        if request.GET.get('date'):
            initial_data['date'] = request.GET.get('date')
        if request.GET.get('time_slot'):
            initial_data['time_slot'] = request.GET.get('time_slot')
        if request.GET.get('party_size'):
            initial_data['party_size'] = request.GET.get('party_size')
        
        form = BookingForm(restaurant=restaurant, initial=initial_data)
    
    # Get available time slots for display
    time_slots = TimeSlot.objects.filter(
        restaurant=restaurant,
        is_active=True
    ).order_by('time')
    
    context = {
        'form': form,
        'restaurant': restaurant,
        'time_slots': time_slots,
    }
    
    return render(request, 'bookings/create_booking.html', context)


@login_required
def booking_detail(request, booking_id):
    """View booking details."""
    booking = get_object_or_404(
        Booking.objects.select_related('customer', 'restaurant', 'time_slot'),
        id=booking_id
    )
    
    # Check if user can view this booking
    if not request.user.is_staff and booking.customer != request.user:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('dashboard')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def edit_booking(request, booking_id):
    """Edit an existing booking."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permissions
    if not request.user.is_staff and booking.customer != request.user:
        messages.error(request, 'You do not have permission to edit this booking.')
        return redirect('dashboard')
    
    # Check if booking can be edited
    if not booking.can_cancel():
        messages.error(request, 'This booking cannot be edited.')
        return redirect('bookings:booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        form = BookingForm(
            request.POST, 
            instance=booking,
            restaurant=booking.restaurant
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('bookings:booking_detail', booking_id=booking.id)
        else:
            messages.error(request, 'Update failed. Please correct the errors.')
    else:
        form = BookingForm(instance=booking, restaurant=booking.restaurant)
    
    context = {
        'form': form,
        'booking': booking,
    }
    
    return render(request, 'bookings/edit_booking.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permissions
    if not request.user.is_staff and booking.customer != request.user:
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        if booking.cancel():
            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'Booking cannot be cancelled.')
        return redirect('bookings:booking_detail', booking_id=booking.id)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/cancel_booking.html', context)


@login_required
def my_bookings(request):
    """View user's own bookings."""
    user = request.user
    bookings = Booking.objects.filter(
        customer=user
    ).select_related('restaurant', 'time_slot').order_by('-date', '-time_slot__time')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'total_bookings': bookings.count(),
    }
    
    return render(request, 'bookings/my_bookings.html', context)


def restaurant_info(request):
    """Display restaurant information and availability."""
    try:
        restaurant = Restaurant.objects.get(is_active=True)
    except Restaurant.DoesNotExist:
        messages.error(request, 'Restaurant information not available.')
        return redirect('home')
    
    # Get time slots
    time_slots = TimeSlot.objects.filter(
        restaurant=restaurant,
        is_active=True
    ).order_by('time')
    
    # Get today's date for availability check
    today = timezone.now().date()
    
    context = {
        'restaurant': restaurant,
        'time_slots': time_slots,
        'today': today,
    }
    
    return render(request, 'bookings/restaurant_info.html', context)


def check_availability(request):
    """Check availability for a specific date and party size."""
    try:
        restaurant = Restaurant.objects.get(is_active=True)
    except Restaurant.DoesNotExist:
        messages.error(request, 'No active restaurant found.')
        return redirect('home')
    
    availability_data = None
    selected_date = None
    selected_party_size = None
    
    if request.method == 'POST':
        form = AvailabilityCheckForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            selected_party_size = form.cleaned_data['party_size']
            
            # Get all time slots for the restaurant
            time_slots = TimeSlot.objects.filter(
                restaurant=restaurant,
                is_active=True
            ).order_by('time')
            
            # Calculate availability for each time slot
            availability_data = []
            max_available_capacity = 0
            for time_slot in time_slots:
                available_capacity = restaurant.get_capacity_for_date_time(
                    selected_date, time_slot
                )
                if available_capacity > max_available_capacity:
                    max_available_capacity = available_capacity
                # Determine availability status
                if available_capacity >= selected_party_size:
                    status = 'available'
                    status_text = f'{available_capacity} seats available'
                    status_class = 'success'
                elif available_capacity > 0:
                    status = 'limited'
                    status_text = f'Only {available_capacity} seats available'
                    status_class = 'warning'
                else:
                    status = 'unavailable'
                    status_text = 'Fully booked'
                    status_class = 'danger'
                
                availability_data.append({
                    'time_slot': time_slot,
                    'available_capacity': available_capacity,
                    'status': status,
                    'status_text': status_text,
                    'status_class': status_class,
                })
        else:
            max_available_capacity = 0
    else:
        form = AvailabilityCheckForm()
        max_available_capacity = 0
    
    context = {
        'form': form,
        'restaurant': restaurant,
        'availability_data': availability_data,
        'selected_date': selected_date,
        'selected_party_size': selected_party_size,
        'max_available_capacity': max_available_capacity,
    }
    
    return render(request, 'bookings/check_availability.html', context) 