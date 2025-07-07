from django.shortcuts import render
from restaurants.models import Restaurant

# NOTE: Requires 'home.html' in a templates directory at the project level.
# Place 'home.html' in a 'templates' folder at the project root or in an app.


def home(request):
    """
    Renders the home page with restaurant information.
    
    **Context**
    ``restaurant``
        The :model:`restaurants.Restaurant` instance if available, else None.
    
    **Template:**
    :template:`home.html`
    """
    try:
        restaurant = Restaurant.objects.get(is_active=True)
    except Restaurant.DoesNotExist:
        restaurant = None
    
    context = {
        'restaurant': restaurant,
    }
    
    return render(request, 'home.html', context) 