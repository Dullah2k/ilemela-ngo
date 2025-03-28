from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django_filters.views import FilterView
from .filters import ProjectFilter
from .models import Project
from .forms import ProjectForm

@login_required
def project_create(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			project = form.save(commit=False)
			project.organization = request.user
			project.save()
			return redirect('project:project_list')
	else:
		form = ProjectForm()

	context = {
		'form': form,
		'title': _('Create Project'),
		'section':'project',
	}
	
	return render(request, 'project/create.html', context)

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

	return render(request, 'project/list.html', {
		'filter': project_filter,
		'is_admin': request.user.is_staff,
		'section':'project',
	})

@login_required
def project_details(request, pk):
	project = get_object_or_404(Project, pk=pk)
	
	# Allow only project owners or admins
	if not (request.user.is_staff or project.organization == request.user):
		return redirect('permission_denied')
	
	return render(request, 'project/detail.html', {'project': project, 'section':'project',})

@login_required
def project_edit(request, pk):
	project = get_object_or_404(Project, pk=pk)
	
	# Allow only project owners or admins to edit
	if not (request.user.is_staff or project.organization == request.user):
		return redirect('permission_denied')
	
	if request.method == 'POST':
		form = ProjectForm(request.POST, instance=project)
		if form.is_valid():
			form.save()
			return redirect('project:project_details', pk=project.pk)
	else:
		form = ProjectForm(instance=project)
	
	return render(request, 'project/edit.html', {'form': form, 'title': _('Edit Project'), 'section':'project',})

