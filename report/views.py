from datetime import timezone
from django.contrib.auth.decorators import login_required
from django.db import models
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .filters import ReportFilter
from project.models import Project
from .forms import ReportForm
from . models import Report, ReportPhoto

@login_required
@transaction.atomic
def report_create(request, project_id):
    # Verify organization ownership
    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.organization:
        return redirect('permission_denied')
    
    # Initialize formsets
    ReportPhotoFormSet = inlineformset_factory(
        Report,
        ReportPhoto,
        fields=('photo', 'caption'),
        extra=5,
        max_num=20,
        can_delete=False
    )

    if request.method == 'POST':
        report_form = ReportForm(request.POST, project=project)
        photo_formset = ReportPhotoFormSet(
            request.POST, 
            request.FILES,
            queryset=ReportPhoto.objects.none()
        )

        if report_form.is_valid() and photo_formset.is_valid():
            # Validate minimum photos
            if len(photo_formset.cleaned_data) < 5:
                messages.error(request, "At least 5 photos are required")
                return render(request, 'reports/report_create.html', {
                    'report_form': report_form,
                    'photo_formset': photo_formset,
                    'project': project
                })

            try:
                # Save report
                report = report_form.save(commit=False)
                report.project = project
                report.save()

                # Save photos
                photos = photo_formset.save(commit=False)
                for photo in photos:
                    photo.report = report
                    photo.save()

                messages.success(request, "Report created successfully!")
                return redirect('project:report_detail', pk=report.pk)

            except Exception as e:
                messages.error(request, f"Error saving report: {str(e)}")

    else:
        # Initialize new form with project context
        initial = {'year': timezone.now().year}
        report_form = ReportForm(project=project, initial=initial)
        photo_formset = ReportPhotoFormSet(queryset=ReportPhoto.objects.none())

    context = {
        'report_form': report_form,
        'photo_formset': photo_formset,
        'project': project,
        'remaining_budget': project.remaining_budget
    }
    return render(request, 'report/create.html', context)

def select_project_for_report(request):
    if request.user.is_staff:
        return redirect('permission_denied')
    
    projects = Project.objects.filter(
        organization=request.user,
        status__in=[Project.Status.ONGOING, Project.Status.PLANNING]
    )
    
    return render(request, 'report/select_project.html', {
        'projects': projects
    })

@login_required
def report_list(request):
    user = request.user
    queryset = Report.objects.all().select_related('project')
    
    # Organization sees only their reports
    if not user.is_staff:
        queryset = queryset.filter(project__organization=user)
    
    # Apply filters
    report_filter = ReportFilter(request.GET, queryset=queryset)
    filtered_reports = report_filter.qs
    
    # Budget Summary Calculations
    projects = Project.objects.filter(reports__in=filtered_reports).distinct()
    
    total_budget = projects.aggregate(
        total=models.Sum('budget')
    )['total'] or 0
    
    total_spent = projects.aggregate(
        total=models.Sum('reports__amount_used')
    )['total'] or 0
    
    summary = {
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining_budget': total_budget - total_spent,
        'utilization': (total_spent / total_budget * 100) if total_budget else 0
    }

    # Pagination
    paginator = Paginator(filtered_reports, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': report_filter,
        'page_obj': page_obj,
        'summary': summary,
        'is_admin': user.is_staff
    }
    return render(request, 'report/list.html', context)

@login_required
def export_reports(request):
    user = request.user
    queryset = Report.objects.all().select_related('project')
    
    if not user.is_staff:
        queryset = queryset.filter(project__organization=user)
    
    report_filter = ReportFilter(request.GET, queryset=queryset)
    filtered_reports = report_filter.qs

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports_export.csv"'
    
    writer = csv.writer(response)
    
    # CSV Headers
    headers = [
        'Project Name', 'Quarter', 'Year', 'Report Title',
        'Amount Used (TZS)', 'Submission Date'
    ]
    
    if user.is_staff:
        headers.insert(0, 'Organization')
    
    writer.writerow(headers)
    
    # CSV Data
    for report in filtered_reports:
        row = [
            report.project.name,
            report.get_quarter_display(),
            report.year,
            report.title,
            report.amount_used,
            report.created_at.strftime("%Y-%m-%d")
        ]
        if user.is_staff:
            row.insert(0, str(report.project.organization))
        writer.writerow(row)
    
    return response

