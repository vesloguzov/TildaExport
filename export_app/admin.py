from django.contrib import admin

from .models import Project, Page, TildaRequest

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'descr')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'descr')

@admin.register(TildaRequest)
class TildaRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'request_count', 'base_url')