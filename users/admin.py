from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Inline admin interface for the UserProfile model, allowing editing of
    user profiles directly within the User admin page.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


class UserAdmin(BaseUserAdmin):
    """
    Custom User admin that includes the UserProfile inline and customizes
    list display, filters, and search fields for user management.
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register UserProfile separately
admin.site.register(UserProfile)
