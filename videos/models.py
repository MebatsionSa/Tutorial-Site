from django.db import models
from authentication.models import User
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
    department_short_name = models.ForeignKey(
        Department,
        default='D',
        on_delete=models.CASCADE)
    course_description = models.CharField(max_length=200)
    course_created_at = models.DateTimeField(auto_now=True)
    course_code = models.CharField(max_length=200,help_text='eg. CSE0000')

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.course_name

class Video(models.Model):
    video_title = models.CharField(max_length=200)
    course_code = models.ForeignKey(
        Course,
        default='C',
        on_delete=models.CASCADE
    )
    video_file = models.FileField(upload_to='videos/uploads/',default='null')
    publication_date = models.DateTimeField(auto_now=True)
    published_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='published',
        default='1')
        
    class Meta:
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.video_title

    """def published_by(model, request):
        obj = model.objects.latest('pk')
        if obj.published is None:
            obj.published_by = request.User
        obj.save()"""