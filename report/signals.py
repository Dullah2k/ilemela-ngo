from django.db.models.signals import m2m_changed
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.forms import ValidationError
from django.db import models
from . models import ReportPhoto

@receiver(models.signals.pre_save, sender=ReportPhoto)
def validate_photo_count(sender, instance, **kwargs):
	# Validate minimum 5 photos
	if instance.report.photos.count() < 5 and not instance.pk:
		raise ValidationError(_("At least 5 photos required"))
	
	# Validate maximum 20 photos
	if instance.report.photos.count() >= 20 and not instance.pk:
		raise ValidationError(_("Maximum 20 photos allowed per report"))