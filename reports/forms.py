from django import forms
from .models import Report, ReportPhoto

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'quarter', 'year', 'title', 'summary', 
            'activities', 'amount_used', 'outcomes', 'challenges'
        ]
        widgets = {
            'year': forms.NumberInput(attrs={'min': 2020, 'max': 2030}),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.project:
            self.instance.project = self.project
            
        if user and not user.is_staff and 'status' in self.fields:
            del self.fields['status']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = ReportPhoto
        fields = ['photo', 'caption']

PhotoFormSet = forms.inlineformset_factory(
    Report, ReportPhoto, form=PhotoForm, extra=5, min_num=5, validate_min=True
)