from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

class Project(models.Model):
	class Status(models.TextChoices):
		PLANNING = 'PLAN', _('Planning')
		ONGOING = 'ONGO', _('Ongoing')
		COMPLETED = 'COMP', _('Completed')
		SUSPENDED = 'SUSP', _('Suspended')

	class FundingType(models.TextChoices):
		GRANT = 'GRANT', _('Grant')  # Fixed typo (GRANT → GRANT)
		DONATION = 'DON', _('Donation')
		SELF_FUNDED = 'SELF', _('Self-Funded')
		PARTNERSHIP = 'PART', _('Partnership')

	# Ward choices for Ilemela District
	class WardChoices(models.TextChoices):
		NYAKATO = 'NYAKATO', _('Nyakato')
		BUSWELU = 'BUSWELU', _('Buswelu')
		ILEMELA = 'ILEMELA', _('Ilemela')
		PASIANSI = 'PASIANSI', _('Pasiansi')
		BUGOBWA = 'BUGOBWA', _('Bugogwa')  # Fixed typo (Bugogwa → BUGOBWA)
		SANGABUYE = 'SANGABUYE', _('Sangabuye')
		MECCO = 'MECCO', _('MECCO')
		BUZURUGA = 'BUZURUGA', _('Buzuruga')
		NYASAKA = 'NYASAKA', _('Nyasaka')
		KAHAMA = 'KAHAMA', _('Kahama')
		KISEKE = 'KISEKE', _('Kiseke')
		KAYENZE = 'KAYENZE', _('Kayenze')
		SHIBULA = 'SHIBULA', _('Shibula')
		KAWEEKAMO = 'KAWEEKAMO', _('Kawekamo')
		KITANGIRI = 'KITANGIRI', _('Kitangiri')
		KIRUMBA = 'KIRUMBA', _('Kirumba')
		NYAMANORO = 'NYAMANORO', _('Nyamanoro')
		IBUNGILO = 'IBUNGILO', _('Ibungilo')
		NYAMHONGOLO = 'NYAMHONGOLO', _('Nyamhongolo')

	name = models.CharField(_("Project Name"), max_length=255)
	description = models.TextField(_("Project Description"))
	organization = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='projects',
		on_delete=models.CASCADE
	)

	# Project Details
	start_date = models.DateField(_("Start Date"))
	end_date = models.DateField(_("End Date"), blank=True, null=True)
	status = models.CharField(
		_("Project Status"),
		max_length=4,
		choices=Status.choices,
		default=Status.PLANNING
	)
	funding_type = models.CharField(
		_("Funding Type"),
		max_length=5,
		choices=FundingType.choices,
		default=FundingType.GRANT
	)
	budget = models.DecimalField(
		_("Project Budget (TZS)"),
		max_digits=14,
		decimal_places=2,
		blank=True,
		null=True
	)

	# Beneficiaries
	men = models.IntegerField(_("Men Beneficiaries"), default=0)  
	women = models.IntegerField(_("Women Beneficiaries"), default=0)
	youth = models.IntegerField(_("Youth Beneficiaries"), default=0)

	# Location
	district = models.CharField(
		_("District"),
		max_length=20,
		default="Ilemela",
		editable=False  # Prevents editing in admin/forms
	)
	ward = models.CharField(
		_("Ward"),
		max_length=20,
		choices=WardChoices.choices
	)
	street = models.CharField(_("Street"), max_length=100)

	# Timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = _("Project")
		verbose_name_plural = _("Projects")
		ordering = ['-created_at']
		indexes = [
			models.Index(fields=['status']),
			models.Index(fields=['organization']),
		]

	def __str__(self):
		return f"{self.name} - {self.organization}"

	def clean(self):
		if self.end_date and self.end_date < self.start_date:
			raise ValidationError(_("End date cannot be before start date."))

	def is_active(self):
		return self.status == self.Status.ONGOING

	@property
	def total_beneficiaries(self):
		return self.men + self.women + self.youth
	
	@property
	def total_spent(self):
		return self.reports.aggregate(total=Sum('amount_used'))['total'] or 0

	@property
	def remaining_budget(self):
		if self.budget:
			return self.budget - self.total_spent
		return None

	@property
	def budget_utilization(self):
		if self.budget and self.total_spent:
			return (self.total_spent / self.budget) * 100
		return 0
	
	