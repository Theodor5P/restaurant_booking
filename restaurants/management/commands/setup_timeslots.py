from django.core.management.base import BaseCommand
from restaurants.models import Restaurant, TimeSlot
from datetime import time


class Command(BaseCommand):
    help = 'Set up initial time slots for the restaurant'

    def handle(self, *args, **options):
        # Create default restaurant if it doesn't exist
        restaurant, created = Restaurant.objects.get_or_create(
            name="Sample Restaurant",
            defaults={
                'description': 'A wonderful restaurant for dining',
                'address': '123 Main Street, City, State 12345',
                'phone': '+1-555-0123',
                'email': 'info@samplerestaurant.com',
                'total_capacity': 40,
                'opening_time': time(17, 0),
                'closing_time': time(22, 0),
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created restaurant: {restaurant.name}')
            )

        # Create time slots
        time_slots = [
            time(17, 0),  # 17:00
            time(18, 0),  # 18:00
            time(19, 0),  # 19:00
            time(20, 0),  # 20:00
            time(21, 0),  # 21:00
        ]

        for slot_time in time_slots:
            time_slot, created = TimeSlot.objects.get_or_create(
                restaurant=restaurant,
                time=slot_time,
                defaults={'is_active': True}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created time slot: {slot_time}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully set up restaurant and time slots')
        ) 