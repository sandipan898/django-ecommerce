from django import forms 
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class SignupUserForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=False, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    first_name = forms.CharField(
        label="First name", 
        required=False, 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    last_name = forms.CharField(
        label="Last name", 
        required=False, 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                #'style': 'width: 500px',
                'autocomplete': 'new-password',
            }
        ), 
        help_text=password_validators_help_text_html()
    )

    password2 = forms.CharField(
        label="Re-enter Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
            }
        ), 
        help_text=("Enter the same password as before, for verification.")
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        
        def clean_username(self):
            username = self.cleaned_data['username']
            if len(username) < 2:
                raise forms.ValidationError("Username is too short")
            elif User.objects.get_object_or_404(username=username):
                raise forms.ValidationError("This username is already taken")
            return username
