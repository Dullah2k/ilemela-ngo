from django.urls import path
from . import views

app_name = "organization"
urlpatterns = [
  path('organizations/', views.organization_list, name='organization_list'),
  path('organizations/<int:id>/', views.organization_detail, name='organization_detail'),
  path('organizations/edit/<int:id>/', views.organization_edit, name='organization_edit'),
  path('organizations/edit/', views.organization_edit, name='organization_edit_self'),
]