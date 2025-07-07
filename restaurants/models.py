from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import time


class Restaurant(models.Model):
    """
    Stores a single restaurant entry with configuration and capacity
    information.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    total_capacity = models.IntegerField(
        default=40,
        validators=[MinValueValidator(1), MaxValueValidator(200)]
    )
    opening_time = models.TimeField(default=time(17, 0))
    closing_time = models.TimeField(default=time(22, 0))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name

    @property
    def available_time_slots(self):
        """Return all active time slots for this restaurant."""
        return self.timeslots.filter(is_active=True)

    def get_capacity_for_date_time(self, date, time_slot):
        """Get available capacity for a specific date and time slot."""
        # Import here to avoid circular imports
        from bookings.models import Booking
        
        # Get total bookings for this date and time
        total_booked = Booking.objects.filter(
            restaurant=self,
            date=date,
            time_slot=time_slot,
            status='confirmed'
        ).aggregate(total=models.Sum('party_size'))['total'] or 0
        
        return self.total_capacity - total_booked


class TimeSlot(models.Model):
    """
    Stores a single time slot entry related to :model:`restaurants.Restaurant`.
    """
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='timeslots'
    )
    time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['restaurant', 'time']
        ordering = ['time']
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'

    def __str__(self):
        return f"{self.restaurant.name} - {self.time.strftime('%H:%M')}"

    @property
    def formatted_time(self):
        """Return formatted time string."""
        return self.time.strftime('%H:%M')
