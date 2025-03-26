from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django_filters.views import FilterView
from .filters import ProjectFilter
from .models import Project
from .forms import ProjectForm

@login_required
def project_create(request):
	if not request.user.is_organization:  # Assuming `is_organization` is a User attribute
		return redirect('permission_denied')
	
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			project = form.save(commit=False)
			project.organization = request.user
			project.save()
			return redirect('project:project_details', pk=project.pk)
	else:
		form = ProjectForm()
	
	return render(request, 'project/create.html', {'form': form, 'title': _('Create Project')})



@login_required
def project_list(request):
	# For admins: Show all projects with filters
	if request.user.is_staff:
		projects = Project.objects.all()
	# For organizations: Show only their projects
	else:
		projects = Project.objects.filter(organization=request.user)

	# Initialize filter with user context
	project_filter = ProjectFilter(
		request.GET, 
		queryset=projects,
		user=request.user  # Pass user to filter to handle organization field
	)

	return render(request, 'project/project_list.html', {
		'filter': project_filter,
		'is_admin': request.user.is_staff
	})