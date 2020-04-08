from django.db import models
from authentication.models import User
from django.utils import timezone
from django.utils.timezone import now

# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=200)
    department_description = models.CharField(max_length=200)
    department_created_at = models.DateTimeField(auto_now=True)
    # department_slug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Department"

    def __str__(self):
        return self.department_name

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    department_name = models.ForeignKey(
        Department, 
        default=1, 
        on_delete=models.CASCADE
    ) # here it means department_id
    course_description = models.CharField(max_length=200)
    course_created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.course_name

class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    pub_date =  models.DateTimeField(auto_now=True)# timezone.now().date() # here it means created_at
    tutorial_content = models.TextField() 
    # tutorial_created_by = 

    course_name = models.ForeignKey(
        Course,
        default=1, 
        on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(User, blank=True)
    # tutorial_slug = models.CharField(max_length=200, default=1,help_text='Please add similar name with tutorial <br>eg. tutorial_title')


    def __str__(self):
        return self.tutorial_title