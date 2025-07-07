from django.shortcuts import render, get_object_or_404
from .models import Restaurant, TimeSlot


def restaurant_list(request):
    """List all restaurants."""
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, 'restaurants/restaurant_list.html', {
        'restaurants': restaurants
    })


def restaurant_detail(request, restaurant_id):
    """Show restaurant details."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
    time_slots = restaurant.available_time_slots
    return render(request, 'restaurants/restaurant_detail.html', {
        'restaurant': restaurant,
        'time_slots': time_slots
    })
