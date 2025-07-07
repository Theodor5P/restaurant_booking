from django.contrib import admin
from .models import Restaurant, TimeSlot


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'total_capacity', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'address')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Configuration', {
            'fields': ('total_capacity', 'opening_time', 'closing_time', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'time', 'is_active', 'created_at')
    list_filter = ('restaurant', 'is_active', 'created_at')
    search_fields = ('restaurant__name',)
    ordering = ('restaurant', 'time')
