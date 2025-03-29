from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from project.models import Project
from .models import Report
from .forms import ReportForm, PhotoFormSet
from .filters import ReportFilter
from .models import ReportPhoto

@login_required
def report_create(request, project_id):
  project = get_object_or_404(Project, pk=project_id, organization=request.user)
  
  if request.method == 'POST':
    form = ReportForm(request.POST, user=request.user, project=project)
    form_valid = form.is_valid()
    report = None

    if form_valid:
      report = form.save(commit=False)
      report.project = project
      report.status = 'SUBM' if request.user.is_staff else 'DRAFT'

    # Always create formset with report instance
    formset = PhotoFormSet(
      request.POST,
      request.FILES,
      instance=report or Report(project=project)
    )

    if form_valid and formset.is_valid():
      try:
        with transaction.atomic():
          # Save report first
          report.save()
          # Save formset with proper instance
          saved_formset = PhotoFormSet(
              request.POST,
              request.FILES,
              instance=report
          )
          saved_formset.save()
          return redirect('reports:report_list')
      except Exception as e:
        form.add_error(None, str(e))
    else:
      # Handle invalid form/formset
      pass
  else:
    # GET request
    form = ReportForm(user=request.user, project=project)
    formset = PhotoFormSet(instance=Report(project=project))

  context = {
    'form': form,
    'formset': formset,
    'project': project,
    'section': 'report',
  }
  return render(request, 'reports/create.html', context)

@login_required
def report_list(request):
  # Base queryset
  if request.user.is_staff:
    reports = Report.objects.all().select_related('project')
  else:
    # Include all reports for organization's projects regardless of status
    reports = Report.objects.filter(
      project__organization=request.user
    ).select_related('project')

  # Apply filters
  report_filter = ReportFilter(request.GET, queryset=reports, request=request)
  filtered_reports = report_filter.qs
  
  # Pagination
  paginator = Paginator(filtered_reports, 25)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'filter': report_filter,
    'page_obj': page_obj,
    'section': 'report',
    'is_admin': request.user.is_staff
  }

  return render(request, 'reports/list.html', context)