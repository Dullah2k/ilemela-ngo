from django.contrib import admin
from .models import OrganizationProfile

@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'registration_number', 'registration_certificate', 'photo', 'phone_number', 'is_verified', 'website', 'annual_budget', 'registration_date', 'date_established' ]
  
  raw_id_fields = ['user']