from django.test import TestCase
from unittest.mock import Mock
from django.utils import timezone
from .forms import BookingForm


class BookingFormTest(TestCase):
    def setUp(self):
        self.restaurant = Mock()
        self.restaurant.get_capacity_for_date_time.return_value = 10
        self.restaurant.total_capacity = 10
        self.restaurant.__str__ = lambda s: 'Testaurant'

        self.time_slot = Mock()
        self.time_slot.pk = 1
        self.time_slot.__str__ = lambda s: '18:00'

    def test_valid_booking(self):
        form_data = {
            'date': (
                timezone.now().date() + timezone.timedelta(days=1)
            ).isoformat(),
            'time_slot': self.time_slot,
            'party_size': 4,
            'special_requests': 'Window seat',
        }
        form = BookingForm(data=form_data, restaurant=self.restaurant)
        # Patch the queryset to allow validation
        form.fields['time_slot'].queryset = [self.time_slot]
        self.assertTrue(form.is_valid())

    def test_booking_in_past(self):
        form_data = {
            'date': (
                timezone.now().date() - timezone.timedelta(days=1)
            ).isoformat(),
            'time_slot': self.time_slot,
            'party_size': 2,
            'special_requests': '',
        }
        form = BookingForm(data=form_data, restaurant=self.restaurant)
        form.fields['time_slot'].queryset = [self.time_slot]
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_exceeding_capacity(self):
        form_data = {
            'date': (
                timezone.now().date() + timezone.timedelta(days=1)
            ).isoformat(),
            'time_slot': self.time_slot,
            'party_size': 20,
            'special_requests': '',
        }
        # Only 10 seats available
        self.restaurant.get_capacity_for_date_time.return_value = 10
        form = BookingForm(data=form_data, restaurant=self.restaurant)
        form.fields['time_slot'].queryset = [self.time_slot]
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors) 