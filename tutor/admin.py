from django.contrib import admin
from .models import Tutorial, Department, Course
from authentication.models import User
from django.db import models

# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {"fields": ["tutorial_title", "pub_date", "posted_by"]}),
        ("Course Category", {"fields":["course_code",]}),# course_code?? coursename
        ("Content", {"fields":["tutorial_content", "likes"]}),
    ]
    readonly_fields = [ "pub_date",]

    """def has_change_permission(self, request, obj=None):
        has_class_permission = super(CourseAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(CourseAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True

    def queryset(self, request):
        if request.user.is_superuser:
            return Video.objects.all()
        return Video.objects.filter(posted_by=request.user.id)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.posted_by = request.user
        obj.save()"""

"""    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
"""
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'department_name', 'course_description', 'course_code')

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(CourseAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(CourseAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_description', 'department_short_name')

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(DepartmentAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(DepartmentAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)

admin.site.register(Tutorial, TutorialAdmin)