from django.db import models
from authentication.models import User
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

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    department_name = models.ForeignKey(
        Department, 
        default="C", 
        on_delete=models.CASCADE
    ) # here it means department_id
    course_description = models.CharField(max_length=200)
    course_created_at = models.DateTimeField(auto_now=True)
    course_code = models.CharField(max_length=200,
         help_text='eg. CSE0000')

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.course_name

class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    pub_date =  models.DateTimeField(auto_now=True)# timezone.now().date() # here it means created_at
    tutorial_content = models.TextField() 
    # tutorial_created_by = models.CharField(max_length=200, default='ASTU')

    course_code = models.ForeignKey(
        Course,
        default="T", 
        on_delete=models.CASCADE,
    )
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    # tutorial_slug = models.CharField(max_length=200, default=1,help_text='Please add similar name with tutorial <br>eg. tutorial_title')
    posted_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='posts',
        default='1')

    def __str__(self):
        return self.tutorial_title

    def total_likes(self):
        return self.likes.count()

    def who_liked(self):
        return self.likes.all()

    def get_absolute_url(self):
        return reverse('tutor:tutorial',
                        args=[self.course_code.department_name.department_short_name,
                        self.course_code.course_code,self.id]
                        )