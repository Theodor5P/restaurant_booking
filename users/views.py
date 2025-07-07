from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def profile(request):
    """User profile view."""
    return render(request, 'users/profile.html')


@login_required
def dashboard(request):
    """User dashboard view."""
    return render(request, 'users/dashboard.html')
