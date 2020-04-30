from django.contrib import admin
from .models import Department, Semester, Course, Book
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'course_code', 'book_file')

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(BookAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(BookAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'semester_name', 'course_description', 'course_code')

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

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester_name', 'department_id')

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(SemesterAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(SemesterAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return False
        return 

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

admin.site.register(Book, BookAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Department, DepartmentAdmin)
