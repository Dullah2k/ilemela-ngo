from django.urls import path
from . import views

app_name = "reports"
urlpatterns = [
  path('projects/<int:project_id>/reports/create/', views.report_create, name='report_create'),
  path('reports/', views.report_list, name='report_list'),
]