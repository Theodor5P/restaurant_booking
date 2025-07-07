from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    # Restaurant views
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('dashboard/', views.restaurant_dashboard, name='dashboard'),
    
    # Time slots
    path('time-slots/', views.time_slot_list, name='time_slot_list'),
] 