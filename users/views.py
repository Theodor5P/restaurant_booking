from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import UserRegistrationForm, UserProfileUpdateForm, UserUpdateForm
from bookings.models import Booking


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                # Log the user in
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to our restaurant booking system.')
                return redirect('users:dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """User login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')


@login_required
def user_logout(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard view."""
    user = request.user
    profile = user.profile
    
    # Get user's bookings
    upcoming_bookings = Booking.objects.filter(
        customer=user,
        status='confirmed'
    ).order_by('date', 'time_slot__time')[:5]
    
    past_bookings = Booking.objects.filter(
        customer=user
    ).exclude(status='confirmed').order_by('-date', '-time_slot__time')[:5]
    
    context = {
        'user': user,
        'profile': profile,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
    }
    
    return render(request, 'users/dashboard.html', context)


@login_required
def profile(request):
    """User profile view and update."""
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Profile update failed. Please correct the errors.')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def booking_history(request):
    """User booking history view."""
    user = request.user
    bookings = Booking.objects.filter(customer=user).order_by('-date', '-time_slot__time')
    
    context = {
        'bookings': bookings,
        'user': user,
    }
    
    return render(request, 'users/booking_history.html', context)
