import django_filters
from django import forms
from .models import Report, Project

class ReportFilter(django_filters.FilterSet):
    YEAR_CHOICES = [(y, y) for y in range(2020, 2031)]
    QUARTER_CHOICES = Report.Quarter.choices
    
    project__status = django_filters.ChoiceFilter(
        choices=Project.Status.choices,
        label="Project Status"
    )
    year = django_filters.ChoiceFilter(choices=YEAR_CHOICES)
    quarter = django_filters.ChoiceFilter(choices=QUARTER_CHOICES)
    status = django_filters.ChoiceFilter(choices=Report.Status.choices)
    submission_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )
    project__funding_type = django_filters.ChoiceFilter(
        choices=Project.FundingType.choices,
        label="Funding Type"
    )
    project__ward = django_filters.ModelChoiceFilter(
        queryset=Project.objects.values_list('ward', flat=True).distinct(),
        widget=forms.Select,
        label="Ward"
    )
    project__start_date = django_filters.DateFromToRangeFilter(
        field_name='project__start_date',
        label='Project Date Range',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Report
        fields = {
            'project__organization': ['exact'],
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.request.user.is_staff:
            del self.filters['project__organization']
            del self.filters['status']