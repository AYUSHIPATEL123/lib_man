from django.contrib.auth.forms import UserCreationForm
from .models import User, Book, BookIssue
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'role', 'password1', 'password2']
    
    
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = ['status',]        
               
              