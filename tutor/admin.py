from django.contrib import admin
from .models import Tutorial, Department, Course
from authentication.models import User
from django.db import models

# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {"fields": ["tutorial_title", "pub_date",]}),
        ("Course Category", {"fields":["course_name",]}),
        ("Content", {"fields":["tutorial_content", "likes"]}),
    ]
    readonly_fields = [ "pub_date",]

"""    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
"""
admin.site.register(Department)
admin.site.register(Course)

admin.site.register(Tutorial, TutorialAdmin)