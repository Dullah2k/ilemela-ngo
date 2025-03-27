from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Sum
from project.models import Project
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError

class Report(models.Model):
  class Quarter(models.IntegerChoices):
    Q1 = 1, _('Q1 (January - March)')
    Q2 = 2, _('Q2 (April - June)')
    Q3 = 3, _('Q3 (July - September)')
    Q4 = 4, _('Q4 (October - December)')

  class Status(models.TextChoices):
    DRAFT = 'DRAFT', _('Draft')
    SUBMITTED = 'SUBM', _('Submitted')
    APPROVED = 'APPR', _('Approved')
    REJECTED = 'REJ', _('Rejected')

  project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    related_name='reports'
  )
  quarter = models.IntegerField(choices=Quarter.choices)
  year = models.PositiveIntegerField(
    validators=[
      MinValueValidator(2020),
      MaxValueValidator(2030)
    ]
  )
  title = models.CharField(_("Report Title"), max_length=200)
  status = models.CharField(
    max_length=5,
    choices=Status.choices,
    default=Status.DRAFT
  )
  summary = models.TextField(_("Executive Summary"))
  activities = models.TextField(_("Activities Conducted"))
  amount_used = models.DecimalField(
    _("Amount Used (TZS)"),
    max_digits=14,
    decimal_places=2
  )
  outcomes = models.TextField(_("Outcomes and Impact"))
  challenges = models.TextField(_("Challenges and Solutions"))
  submission_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ['project', 'quarter', 'year']
    ordering = ['-year', '-quarter']

  def clean(self):
    # Add check for project existence
    if not self.project_id:
        raise ValidationError(_("Report must be associated with a project"))
        
    if self.amount_used > self.project.budget:
        raise ValidationError(
            _("Amount used exceeds project budget of %(budget)s TZS"),
            params={'budget': self.project.budget}
        )

class ReportPhoto(models.Model):
  report = models.ForeignKey(
    Report,
    on_delete=models.CASCADE,
    related_name='photos'
  )
  photo = models.ImageField(
    upload_to='reports/photos/%Y/%m/',
    validators=[
      FileExtensionValidator(['jpg', 'png', 'jpeg'])
    ]
  )
  caption = models.CharField(max_length=200, blank=True)

  def clean(self):
    # Ensure minimum 5 photos per report
    if self.report.photos.count() >= 4:  # Current photo will make 5
      return
    if self.report.photos.count() < 4 and not self.pk:
      raise ValidationError(
        _("At least 5 photos are required for each report")
      )
    