# project/filters.py
import django_filters
from django.contrib.auth import get_user_model
from .models import Project
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class ProjectFilter(django_filters.FilterSet):
	organization = django_filters.ModelChoiceFilter(
		queryset=User.objects.filter(is_staff=False),  # Organizations are non-staff users
		label=_("Organization")
	)

	class Meta:
		model = Project
		fields = ['ward', 'status', 'funding_type', 'organization']

	def __init__(self, *args, **kwargs):
		# Remove organization filter for non-admin users
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		if not self.user.is_staff:
			self.filters.pop('organization', None)