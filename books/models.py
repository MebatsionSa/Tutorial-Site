from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.urls import reverse
# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=200)
    department_description = models.CharField(max_length=200)
    department_created_at = models.DateTimeField(auto_now=True)
    department_short_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Department"

    def __str__(self):
        return self.department_name

class Semester(models.Model):
    semester_name = models.CharField(max_length=200)
    semester_created_at = models.DateTimeField(auto_now=True)
    department_id = models.ForeignKey(
        Department,
        default=1,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Semester"

    def __str__(self):
        return self.semester_name

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    semester_name = models.ForeignKey(
        Semester, 
        default="S", 
        on_delete=models.CASCADE
    ) # here it means semester_id
    course_description = models.CharField(max_length=200)
    course_created_at = models.DateTimeField(auto_now=True)
    course_code = models.CharField(max_length=200,
         help_text='eg. CSE0000')

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.course_name

class Book(models.Model):
    book_name = models.CharField(max_length=200)
    course_code = models.ForeignKey(
        Course,
        default="C",
        on_delete=models.CASCADE
    )
    book_file = models.FileField(upload_to='books/uploads/',default='null')

    class Meta:
        verbose_name_plural = "Books"

    def __str__(self):
        return self.book_name
