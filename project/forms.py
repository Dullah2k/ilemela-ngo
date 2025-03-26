from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = '__all__'
		exclude = ['organization', 'district', 'created_at', 'updated_at']