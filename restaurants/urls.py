from django.urls import path
from django.http import HttpResponse

def restaurant_list(request):
    return HttpResponse("Restaurant List Page")

def restaurant_detail(request, restaurant_id):
    return HttpResponse(f"Restaurant Detail Page - ID: {restaurant_id}")

app_name = 'restaurants'

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),
    path('<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
] 