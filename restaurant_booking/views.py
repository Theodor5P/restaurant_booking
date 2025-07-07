from django.shortcuts import render

# NOTE: Requires 'home.html' in a templates directory at the project level.
# Place 'home.html' in a 'templates' folder at the project root or in an app.


def home(request):
    return render(request, 'home.html') 