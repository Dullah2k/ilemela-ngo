from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Sum
from project.models import Project

class Report(models.Model):
	class Quarter(models.TextChoices):
		Q1 = 'Q1', _('January - March')
		Q2 = 'Q2', _('April - June')
		Q3 = 'Q3', _('July - September')
		Q4 = 'Q4', _('October - December')

	project = models.ForeignKey(
		Project,
		on_delete=models.CASCADE,
		related_name='reports'
	)
	quarter = models.CharField(
		_("Quarter"),
		max_length=2,
		choices=Quarter.choices
	)
	year = models.PositiveIntegerField(_("Year"))
	title = models.CharField(_("Report Title"), max_length=200)
	summary = models.TextField(_("Executive Summary"))
	activities = models.TextField(_("Activities Conducted"))
	amount_used = models.DecimalField(
		_("Amount Used (TZS)"),
		max_digits=14,
		decimal_places=2
	)
	outcomes = models.TextField(_("Outcomes and Impact"))
	challenges = models.TextField(_("Challenges and Solutions"))
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ['project', 'quarter', 'year']
		ordering = ['-year', 'quarter']
		verbose_name = _("Quarterly Report")
		verbose_name_plural = _("Quarterly Reports")

	def __str__(self):
		return f"{self.project} - {self.get_quarter_display()} {self.year}"

	def clean(self):
		# Validate maximum 4 reports per year
		existing_reports = Report.objects.filter(
				project=self.project,
				year=self.year
		).count()
		if existing_reports >= 4:
				raise ValidationError(_("Maximum 4 reports per year allowed"))

class ReportPhoto(models.Model):
	report = models.ForeignKey(
		Report,
		on_delete=models.CASCADE,
		related_name='photos'
	)
	photo = models.ImageField(
		_("Project Photo"),
		upload_to='reports/photos/'
	)
	caption = models.CharField(
		_("Photo Caption"),
		max_length=200,
		blank=True
	)

	class Meta:
		verbose_name = _("Report Photo")
		verbose_name_plural = _("Report Photos")

	def __str__(self):
		return f"Photo for {self.report}"
	
	