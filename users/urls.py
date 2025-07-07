from django.urls import path
from django.http import HttpResponse

def profile(request):
    return HttpResponse("User Profile Page")

def dashboard(request):
    return HttpResponse("User Dashboard Page")

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
] 