from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'completed', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['completed']
    ordering = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 10
    list_editable = ['completed']
