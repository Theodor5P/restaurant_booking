from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface for the Booking model, providing list display, filters,
    search, and custom fieldsets for managing bookings in the admin panel.
    """
    list_display = ('customer', 'restaurant', 'date', 'time_slot', 'party_size', 'status', 'created_at')
    list_filter = ('status', 'date', 'restaurant', 'time_slot', 'created_at')
    search_fields = ('customer__username', 'customer__email', 'restaurant__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ('-date', '-time_slot__time')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('customer', 'restaurant', 'date', 'time_slot', 'party_size')
        }),
        ('Details', {
            'fields': ('special_requests', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """
        Returns a queryset with related customer, restaurant, and time_slot
        objects selected for performance optimization in the admin list view.
        """
        return super().get_queryset(request).select_related(
            'customer', 'restaurant', 'time_slot'
        ) 