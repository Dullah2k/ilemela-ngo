from django.db import models
from django.conf import settings

class OrganizationProfile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
  registration_number = models.CharField(max_length=20, unique=True)
  phone_number = models.CharField(max_length=15)
  registration_certificate = models.FileField(upload_to='ngo_docs/%Y/%m/%d/', blank=True)
  is_verified = models.BooleanField(default=False)
  website = models.URLField(blank=True)
  annual_budget = models.DecimalField(max_digits=14, decimal_places=2, null=True,blank=True)
  registration_date = models.DateField(null=True, blank=True )
  date_established = models.DateField(null=True, blank=True)

  def __str__(self):
    return f'Profile of {self.user.username}'