from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('user_account.urls', namespace='usser_account')),
  path('', include('organization.urls', namespace='organization')),
  path('', include('project.urls', namespace='project')),
  path('', include('report.urls', namespace='report')),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)