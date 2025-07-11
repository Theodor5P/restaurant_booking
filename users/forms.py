from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with extended profile fields.
    
    Fields:
        - username, email, first_name, last_name, password1, password2, phone_number
    
    Meta:
        model: :model:`auth.User`
        form: :form:`users.UserRegistrationForm`
    """
    phone_number = forms.CharField(
        max_length=15, 
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone Number'}
        )
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 
            'password1', 'password2'
        )
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Username'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name'}
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the registration form and applies Bootstrap styling to all fields.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        """
        Saves the user and associated profile with the provided phone number and role.
        """
        user = super().save(commit)
        user.profile.role = 'customer'
        user.profile.phone_number = self.cleaned_data.get('phone_number', '')
        user.profile.save()
        return user


class UserProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    
    Meta:
        model: :model:`users.UserProfile`
        form: :form:`users.UserProfileUpdateForm`
    """
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'role')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information.
    
    Meta:
        model: :model:`auth.User`
        form: :form:`users.UserUpdateForm`
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        } 