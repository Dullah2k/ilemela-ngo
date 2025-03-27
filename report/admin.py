from django.contrib import admin
from . models import Report, ReportPhoto

class ReportPhotoInline(admin.TabularInline):
	model = ReportPhoto
	extra = 5
	max_num = 20

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
	inlines = [ReportPhotoInline]
	list_display = ['project', 'quarter', 'year']
	readonly_fields = ['created_at', 'updated_at']
	list_filter = ['year', 'quarter']

@admin.register(ReportPhoto)
class ReportPhotoAdmin(admin.ModelAdmin):
	list_display = ['report', 'photo']