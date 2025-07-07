from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Booking(models.Model):
    """
    Stores a single restaurant booking entry related to :model:`auth.User`,
    :model:`restaurants.Restaurant`, and :model:`restaurants.TimeSlot`.
    """
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    customer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    restaurant = models.ForeignKey(
        'restaurants.Restaurant', 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    date = models.DateField()
    time_slot = models.ForeignKey(
        'restaurants.TimeSlot', 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    party_size = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    special_requests = models.TextField(blank=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='confirmed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        # Ensure one booking per customer per date/time combination
        unique_together = ['customer', 'restaurant', 'date', 'time_slot']

    def __str__(self):
        return f"{self.customer.username} - {self.date} {self.time_slot.time}"

    @property
    def is_upcoming(self):
        """Check if booking is in the future."""
        return self.date >= timezone.now().date()

    @property
    def is_today(self):
        """Check if booking is for today."""
        return self.date == timezone.now().date()

    @property
    def is_past(self):
        """Check if booking is in the past."""
        return self.date < timezone.now().date()

    def can_cancel(self):
        """Check if booking can be cancelled (not in the past and confirmed)."""
        return self.is_upcoming and self.status == 'confirmed'

    def cancel(self):
        """Cancel the booking."""
        if self.can_cancel():
            self.status = 'cancelled'
            self.save()
            return True
        return False

    def complete(self):
        """Mark booking as completed."""
        if self.status == 'confirmed':
            self.status = 'completed'
            self.save()
            return True
        return False

    def clean(self):
        """Custom validation for booking."""
        from django.core.exceptions import ValidationError
        
        # Check if required fields are present
        if self.party_size is None:
            raise ValidationError("Party size is required.")
        if self.restaurant is None:
            raise ValidationError("Restaurant is required.")
        if self.restaurant.total_capacity is None:
            raise ValidationError("Restaurant capacity is not set.")
        if self.time_slot is None:
            raise ValidationError("Time slot is required.")
        if self.date is None:
            raise ValidationError("Date is required.")
        
        # Check if date is not in the past
        if self.date < timezone.now().date():
            raise ValidationError("Cannot book for past dates.")
        
        # Check if party size doesn't exceed restaurant capacity
        if self.party_size > self.restaurant.total_capacity:
            raise ValidationError(
                f"Party size cannot exceed restaurant capacity of {self.restaurant.total_capacity}."
            )
        
        # Check if there's enough capacity for this booking
        available_capacity = self.restaurant.get_capacity_for_date_time(
            self.date, self.time_slot
        )
        
        # For existing bookings, exclude current booking from capacity calculation
        if self.pk:
            existing_bookings = Booking.objects.filter(
                restaurant=self.restaurant,
                date=self.date,
                time_slot=self.time_slot,
                status='confirmed'
            ).exclude(pk=self.pk)
        else:
            existing_bookings = Booking.objects.filter(
                restaurant=self.restaurant,
                date=self.date,
                time_slot=self.time_slot,
                status='confirmed'
            )
        
        total_booked = existing_bookings.aggregate(
            total=models.Sum('party_size')
        )['total'] or 0
        
        if total_booked + self.party_size > self.restaurant.total_capacity:
            raise ValidationError(
                f"Insufficient capacity. Only {self.restaurant.total_capacity - total_booked} seats available."
            )

    def save(self, *args, **kwargs):
        """Override save to include validation."""
        self.clean()
        super().save(*args, **kwargs) 