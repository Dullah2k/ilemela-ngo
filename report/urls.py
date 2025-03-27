from django.urls import path
from . import views

app_name = "report"
urlpatterns = [
	# path('reports/create/<int:project_id>/', views.report_create, name='report_create'),
    path('create/', views.select_project_for_report, name='report_create'),
    path('create/<int:project_id>/', views.report_create, name='report_create_project'),
	path('list/', views.report_list, name='report_list'),
	path('export/', views.export_reports, name='export_reports'),
]