from django import forms
from django.contrib.auth.models import User
from .models import OrganizationProfile


class UserRegistrationForm(forms.ModelForm):
  registration_number = forms.CharField(max_length=20)
  phone_number = forms.CharField(max_length=15)
  password = forms.CharField(label='Password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
  
  class Meta:
    model = User
    fields = ['username', 'first_name', 'email']
    labels = {
      'first_name': 'Organization Name'
    }

  def clean_password2(self):
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
      raise forms.ValidationError('Passwords don\'t match.')
    return cd['password2']
  
class OrganizationEditForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email']

class OrganizationProfileEditForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    use_admin_fields = kwargs.pop('use_admin_fields', False)
    super().__init__(*args, **kwargs)
    if not use_admin_fields:
        self.fields.pop('is_verified', None)

  class Meta:
    model = OrganizationProfile
    fields = ['registration_number', 'registration_certificate', 'photo', 
    'phone_number', 'is_verified', 'website', 'annual_budget', 
    'registration_date', 'date_established']
    
    widgets = {
      'registration_date': forms.DateInput(attrs={'type': 'date'}),
      'date_established': forms.DateInput(attrs={'type': 'date'}),
      'annual_budget': forms.NumberInput(attrs={'step': '0.01'}),
    }