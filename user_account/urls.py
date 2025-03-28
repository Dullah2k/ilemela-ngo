from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'user_account'

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('', views.dashboard, name='dashboard'),
  path('register/', views.register, name='register'),
]