from django.forms import ModelForm
from django import forms
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields  = '__all__'
        exclude =[
            'host', 'participants'
        ]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'avatar',
            'first_name',
            'last_name', 
            'email', 
            'username',
            'bio',
        ]

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__ (self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)