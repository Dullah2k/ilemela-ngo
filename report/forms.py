from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Report, Project
from django.utils import timezone

class ReportForm(forms.ModelForm):
	# Year selector with 10-year range
	current_year = timezone.now().year
	YEAR_CHOICES = [(year, year) for year in range(current_year - 5, current_year + 5)]
	
	year = forms.TypedChoiceField(
		label=_("Reporting Year"),
		choices=YEAR_CHOICES,
		coerce=int,
		initial=current_year
	)

	class Meta:
		model = Report
		fields = [
			'quarter', 'year', 'title', 'summary', 
			'activities', 'amount_used', 'outcomes', 'challenges'
		]
		widgets = {
			'quarter': forms.Select(attrs={'class': 'form-select'}),
			'summary': forms.Textarea(attrs={'rows': 4}),
			'activities': forms.Textarea(attrs={'rows': 4}),
			'outcomes': forms.Textarea(attrs={'rows': 4}),
			'challenges': forms.Textarea(attrs={'rows': 4}),
			'amount_used': forms.NumberInput(attrs={
				'step': '1000',
				'min': '0',
				'placeholder': _('Amount in TZS')
			}),
		}
		labels = {
			'amount_used': _("Amount Used (TZS)"),
			'outcomes': _("Outcomes and Impact"),
			'challenges': _("Challenges and Solutions")
		}

	def __init__(self, *args, **kwargs):
		self.project = kwargs.pop('project', None)
		super().__init__(*args, **kwargs)
		
		# Set budget helper text
		if self.project and self.project.budget:
			remaining = self.project.remaining_budget
			self.fields['amount_used'].help_text = _(
				f"Project budget: {self.project.budget:,} TZS | "
				f"Remaining budget: {remaining:,} TZS"
			)

	def clean(self):
		cleaned_data = super().clean()
		
		# Validate budget constraints
		if self.project and 'amount_used' in cleaned_data:
			amount_used = cleaned_data['amount_used']
			remaining = self.project.remaining_budget
			
			if amount_used > remaining:
				self.add_error(
					'amount_used',
					ValidationError(
						_("Amount exceeds remaining budget of %(remaining)s TZS"),
						params={'remaining': remaining}
					)
				)
		
		# Validate quarter/year uniqueness
		if self.project and all(field in cleaned_data for field in ['quarter', 'year']):
			if Report.objects.filter(
				project=self.project,
				quarter=cleaned_data['quarter'],
				year=cleaned_data['year']
			).exclude(pk=self.instance.pk).exists():
				self.add_error(
					'quarter',
					ValidationError(_("Report for this quarter already exists"))
				)
				self.add_error(
					'year',
					ValidationError(_("Report for this year already exists"))
				)

		return cleaned_data