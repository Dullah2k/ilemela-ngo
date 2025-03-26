from django.urls import path
from . import views

app_name = "project"

urlpatterns = [
	path('create/', views.project_create, name='project_create'),
  path('list/', views.project_list, name='project_list'),
]