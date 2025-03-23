from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from user_account.models import OrganizationProfile


def organization_list(request):
  # Filtering
  filter_param = request.GET.get('filter', 'all')
  organizations = OrganizationProfile.objects.select_related('user')
  
  if filter_param == 'verified':
    organizations = organizations.filter(is_verified=True)

  elif filter_param == 'unverified':
    organizations = organizations.filter(is_verified=False)

  # Sorting
  sort_param = request.GET.get('sort')
  if sort_param == 'established':
    organizations = organizations.order_by('date_established')
  elif sort_param == 'registered':
    organizations = organizations.order_by('registration_date')

  context = {
    'organizations': organizations,
    'current_filter': filter_param,
    'current_sort': sort_param,
    'section' : 'organization',
  }

  return render(request, 'organization/list.html', context)

def organization_detail(request, id):
  organization = get_object_or_404(
    OrganizationProfile.objects.select_related('user'), 
    pk=id
  )

  context = {
    'organization': organization,
    'section' : 'organization',
  }
  
  return render(request, 'organization/details.html', context)

