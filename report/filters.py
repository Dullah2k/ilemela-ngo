import django_filters
from django.utils import timezone
from .models import Report, Project

class ReportFilter(django_filters.FilterSet):
    YEAR_CHOICES = [(y, y) for y in range(2010, timezone.now().year + 1)]
    
    year = django_filters.ChoiceFilter(
        field_name='year',
        choices=YEAR_CHOICES,
        label="Report Year"
    )
    
    quarter = django_filters.ChoiceFilter(
        choices=Report.Quarter.choices,
        label="Quarter"
    )
    
    class Meta:
        model = Report
        fields = {
            'project__status': ['exact'],
            'project__ward': ['exact'],
            'project__funding_type': ['exact'],
            'created_at': ['date__gte', 'date__lte']
        }
        labels = {
            'project__status': 'Project Status',
            'project__ward': 'Ward',
            'project__funding_type': 'Funding Type'
        }