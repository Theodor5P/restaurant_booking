from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Restaurant

def get_or_create_profile(user):
    from users.models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def restaurant_list(request):
    """
    Lists all active restaurants.
    
    **Context**
    ``restaurants``
        Queryset of :model:`restaurants.Restaurant`.
    
    **Template:**
    :template:`restaurants/restaurant_list.html`
    """
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, 'restaurants/restaurant_list.html', {
        'restaurants': restaurants
    })


def restaurant_detail(request, restaurant_id):
    """
    Shows details for a single restaurant.
    
    **Context**
    ``restaurant``
        The :model:`restaurants.Restaurant` instance.
    ``time_slots``
        Queryset of :model:`restaurants.TimeSlot` for the restaurant.
    
    **Template:**
    :template:`restaurants/restaurant_detail.html`
    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
    time_slots = restaurant.timeslots.filter(is_active=True).order_by('time')
    
    context = {
        'restaurant': restaurant,
        'time_slots': time_slots,
    }
    
    return render(request, 'restaurants/restaurant_detail.html', context)


@login_required
def restaurant_dashboard(request):
    """
    Displays the staff dashboard for the restaurant.
    
    **Context**
    ``restaurant``
        The :model:`restaurants.Restaurant` instance.
    ``today_bookings``
        Queryset of today's :model:`bookings.Booking`.
    ``upcoming_bookings``
        Queryset of upcoming :model:`bookings.Booking`.
    ``today``
        The current date.
    
    **Template:**
    :template:`restaurants/dashboard.html`
    """
    profile = get_or_create_profile(request.user)
    if not profile.is_staff_member and not request.user.is_staff:
        messages.error(request, 'Access denied. Staff access required.')
        return redirect('home')
    
    try:
        restaurant = Restaurant.objects.get(is_active=True)
    except Restaurant.DoesNotExist:
        messages.error(request, 'No active restaurant found.')
        return redirect('home')
    
    # Get today's bookings
    from django.utils import timezone
    from bookings.models import Booking
    
    today = timezone.now().date()
    today_bookings = Booking.objects.filter(
        restaurant=restaurant,
        date=today,
        status='confirmed'
    ).select_related('customer', 'time_slot').order_by('time_slot__time')
    
    # Get upcoming bookings
    upcoming_bookings = Booking.objects.filter(
        restaurant=restaurant,
        date__gte=today,
        status='confirmed'
    ).select_related('customer', 'time_slot').order_by('date', 'time_slot__time')[:10]
    
    context = {
        'restaurant': restaurant,
        'today_bookings': today_bookings,
        'upcoming_bookings': upcoming_bookings,
        'today': today,
    }
    
    return render(request, 'restaurants/dashboard.html', context)


def time_slot_list(request):
    """
    Lists all time slots for the active restaurant.
    
    **Context**
    ``restaurant``
        The :model:`restaurants.Restaurant` instance.
    ``time_slots``
        Queryset of :model:`restaurants.TimeSlot` for the restaurant.
    
    **Template:**
    :template:`restaurants/time_slot_list.html`
    """
    try:
        restaurant = Restaurant.objects.get(is_active=True)
    except Restaurant.DoesNotExist:
        messages.error(request, 'Restaurant not found.')
        return redirect('home')
    
    time_slots = restaurant.timeslots.filter(is_active=True).order_by('time')
    
    context = {
        'restaurant': restaurant,
        'time_slots': time_slots,
    }
    
    return render(request, 'restaurants/time_slot_list.html', context)
