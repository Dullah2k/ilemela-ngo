from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from project.models import Project
from .models import Report
from .forms import ReportForm, PhotoFormSet
from .filters import ReportFilter

@login_required
def report_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id, organization=request.user)
    
    if request.method == 'POST':
        # Pass project to the form
        form = ReportForm(request.POST, user=request.user, project=project)
        formset = PhotoFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            report = form.save(commit=False)
            # Already set via form, but ensure it's there
            report.project = project  
            report.status = 'SUBM' if request.user.is_staff else 'DRAFT'
            report.save()
            
            formset.instance = report
            formset.save()
            
            return redirect('project:report_detail', pk=report.pk)
    else:
        # Initialize form with project for GET requests
        form = ReportForm(user=request.user, project=project)
        formset = PhotoFormSet()

    context = {
        'form': form,
        'formset': formset,
        'project': project,
    }
    return render(request, 'reports/create.html', context)

@login_required
def report_list(request):
    # Base queryset
    if request.user.is_staff:
        reports = Report.objects.all().select_related('project')
    else:
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
        'is_admin': request.user.is_staff
    }
    return render(request, 'reports/list.html', context)