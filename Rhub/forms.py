from django.forms import ModelForm
from Rhub.models import Feedback

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) == 0:
            raise forms.ValidationError("You cannot leave message field empty.")
        return message

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_count = User.objects.filter(email=email).count()
        
        if email_count > 0:
            raise forms.ValidationError("This email has already been registered.")
        return email
