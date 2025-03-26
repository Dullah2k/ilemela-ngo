from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models

class Project(models.Model):
  class Status(models.TextChoices):
    PLANNING = 'PLAN', _('Planning')
    ONGOING = 'ONGO', _('Ongoing')
    COMPLETED = 'COMP', _('Completed')
    SUSPENDED = 'SUSP', _('Suspended')

  class FundingType(models.TextChoices):
    GRANT = 'GRANT', _('Grant')
    DONATION = 'DON', _('Donation')
    SELF_FUNDED = 'SELF', _('Self-Funded')
    PARTNERSHIP = 'PART', _('Partnership')

  name = models.CharField(_("Project Name"), max_length=255)
  description = models.TextField(_("Project Description"))
  organization = models.ForeignKey(settings.AUTH_USER_MODEL,
    related_name='projects',
    on_delete=models.CASCADE)

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

  men = models.IntegerField(_("Men Beneficiaries"), default=0)  
  women = models.IntegerField(_("Women Beneficiaries"), default=0)
  youth = models.IntegerField(_("Youth Beneficiaries"), default=0)
  
  ward = models.CharField(_("Ward"), max_length=10)
  street = models.CharField(_("Street"), max_length=10)

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
    try:
      return f"{self.organization.organization_profile.registration_number} - {self.get_quarter_display()} {self.year}"
    except AttributeError:
      return f"Report {self.id}"

  def is_active(self):
    return self.status == self.Status.ONGOING
  