from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from user_account.models import OrganizationProfile
from user_account.forms import OrganizationEditForm, OrganizationProfileEditForm


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

@login_required
def organization_edit(request, id=None):
  # Admin can edit any profile, users can only edit their own
  if id and request.user.is_staff:
    profile = get_object_or_404(OrganizationProfile, id=id)
    user_instance = profile.user
  else:
    profile = request.user.organizationprofile
    user_instance = request.user

  if not request.user.is_staff and profile.user != request.user:
    return redirect('organization_detail', id=profile.id)

  if request.method == 'POST':
    user_form = OrganizationEditForm(request.POST, instance=user_instance)
    profile_form = OrganizationProfileEditForm(
      request.POST, 
      request.FILES, 
      instance=profile,
      # Remove is_verified from form when non-admin users submit
      use_admin_fields=request.user.is_staff
    )
    
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, 'Profile updated successfully')
      return redirect('organization:organization_detail', id=profile.id)
    else:
      messages.error(request, 'Error updating profile - please check the form')

  else:
    user_form = OrganizationEditForm(instance=user_instance)
    profile_form = OrganizationProfileEditForm(
      instance=profile,
      # Show is_verified field only for admin users
      use_admin_fields=request.user.is_staff
    )

  return render(request, 'organization/edit.html', {
    'user_form': user_form,
    'profile_form': profile_form,
    'editing_other': id and request.user.is_staff
  })