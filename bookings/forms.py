from django import forms
from django.utils import timezone
from .models import Booking
from restaurants.models import TimeSlot


class BookingForm(forms.ModelForm):
    """
    Form for creating and editing bookings.
    
    Fields:
        - date, time_slot, party_size, special_requests
    
    Meta:
        model: :model:`bookings.Booking`
        form: :form:`bookings.BookingForm`
    """
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().isoformat()
            }
        )
    )
    
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a time slot"
    )
    
    party_size = forms.IntegerField(
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Number of guests'
            }
        )
    )
    
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests or dietary requirements'
            }
        )
    )

    class Meta:
        model = Booking
        fields = ('date', 'time_slot', 'party_size', 'special_requests')
        exclude = ('customer', 'restaurant', 'status', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        """
        Initializes the booking form and filters time slots by restaurant if provided.
        """
        self.restaurant = kwargs.pop('restaurant', None)
        super().__init__(*args, **kwargs)
        
        if self.restaurant:
            # Filter time slots for this restaurant
            self.fields['time_slot'].queryset = TimeSlot.objects.filter(
                restaurant=self.restaurant,
                is_active=True
            )

    def clean_date(self):
        """
        Validates that the booking date is not in the past.
        """
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise forms.ValidationError(
                "Cannot book for past dates."
            )
        return date

    def clean(self):
        """
        Custom validation for booking capacity and availability.
        """
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')
        party_size = cleaned_data.get('party_size')
        
        if date and time_slot and party_size and self.restaurant:
            # Check capacity
            available_capacity = self.restaurant.get_capacity_for_date_time(
                date, time_slot
            )
            
            if party_size > available_capacity:
                raise forms.ValidationError(
                    f"Insufficient capacity. Only {available_capacity} "
                    f"seats available."
                )
        
        return cleaned_data


class BookingFilterForm(forms.Form):
    """
    Form for filtering bookings in the booking list view.
    
    Fields:
        - date_from, date_to, status, time_slot
    """
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Booking.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Time Slots"
    )


class AvailabilityCheckForm(forms.Form):
    """
    Form for checking availability on a specific date.
    
    Fields:
        - date, party_size
    """
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().isoformat()
            }
        ),
        help_text="Select a date to check availability"
    )
    
    party_size = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=2,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Number of guests'
            }
        ),
        help_text="Number of guests for your party"
    )

    def clean_date(self):
        """Validate that the date is not in the past."""
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise forms.ValidationError(
                "Cannot check availability for past dates."
            )
        return date 