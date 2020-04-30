from django.shortcuts import render
from django.http import HttpResponse
from .models import Department, Course, Video
# Create your views here.

def index(request):
    return HttpResponse("I missed aloha!")

def home(request):
    department = Department.objects.all()
    for i in department:
        print(i.department_short_name)
    return render(request,
                  "video/departments.html",
                  {"department":department})

def courses(request, selected_department):
    department = [d.department_short_name for d in Department.objects.all()]
    if selected_department in department:
        courses_of_department = Course.objects.filter(
            department_short_name_id__department_short_name=selected_department
        )
        video_urls = {}
        for each_course in courses_of_department:
            print(each_course.course_name)
            video = Video.objects.filter(
                course_code__course_code=each_course.course_code
            ).earliest('publication_date')
            print(video.id)
            video_urls[each_course] = video.id

    return render(request,
                  "video/courses.html",
                  {"courses":courses_of_department,
                   "videos":video_urls})
                
def videos(request, selected_department, selected_course, selected_video):
    department = [d.department_short_name for d in Department.objects.all()]
    if selected_department in department:
        courses_of_department = Course.objects.filter(
            department_short_name_id__department_short_name=selected_department
        )
        video_urls = {}
        for each_course in courses_of_department:
            print(each_course.course_name)
            video = Video.objects.filter(
                course_code__course_code=each_course.course_code
            ).earliest('publication_date')
            print(video.id)
            video_urls[each_course] = video.id
    video = [v.id for v in Video.objects.all()]
    if selected_video in video:
        selected_url = Video.objects.get(id=selected_video)
        print(selected_url)
        video_related_urls = Video.objects.filter(
            course_code=selected_url.course_code
        ).order_by("video_title")
        selected_url_index = list(video_related_urls).index(selected_url)
        return render(request,
                    "video/tutorial.html",
                    {"video":selected_url,
                     "sidebar":video_related_urls,
                     "selected_url_index":selected_url_index
                     })
    return HttpResponse(f"{selected_video} does not corresponding to anything :(")