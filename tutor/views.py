from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, Course, Department
from authentication.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.


"""def SearchResults(request):
    query = request.GET.get('q')
    course_search_result = Course.objects.filter(Q(course_name__icontains=query))
    tutorial_search_result = Tutorial.objects.filter(Q(tutorial_title__icontains=query))
    tutorial_content_search_result = Tutorial.objects.filter(Q(tutorial_content__icontains=query))
    return render(request,
                  'tutor/search.html',
                  {'tutorial_search_results':tutorial_search_result, 
                   'course_search_results':course_search_result,
                   'tutorial_content_search_results':tutorial_content_search_result})
"""
def home(request):
    d = Department.objects.all()
    """ for i in d:
        print(i.id)"""
    return render(request=request,
    template_name="tutor/departments.html",
    context={"department":d})

def course(request, requested_department):
    department = [d.department_name for d in Department.objects.all()]
    print(department)
    print("El departmente finished #########")
    if requested_department in department:
        matching_course = Course.objects.filter(
            department_name__department_name=requested_department)

        tutorial_urls={} # all tutorials found in requested department
        for each in matching_course.all():
            print(each)
            tutorials = Tutorial.objects.filter(course_name__course_name=each.course_name).earliest('pub_date')
            print(tutorials, tutorials.id)
            tutorial_urls[each]=tutorials.id
            print("After ", each)
        for i in tutorial_urls:
            print(i.id)
        print("forend in course")
        return render(request,
                      "tutor/courses.html",
                      {"tutorial":tutorial_urls})
    return HttpResponse(f"{requested_department} does not correspond to any course :(")

def tutorial(request, requested_department, course_name, requested_url):
    department = [d.department_name for d in Department.objects.all()]
    if requested_department in department:
        matching_course = Course.objects.filter(
            department_name__department_name=requested_department)

        tutorial_urls={} # all tutorials found in requested department
        for each in matching_course.all():
            tutorials = Tutorial.objects.filter(course_name__course_name=each.course_name).earliest('pub_date')
            
            tutorial_urls[each]=tutorials.id
            print(each," + ",tutorials)

        """for k, v in tutorial_urls.items():
            print(k, v)"""

    """values = [k for k in tutorial_urls.values()]
    print(values)"""
    
    tutorial = [t.id for t in Tutorial.objects.all()]
    """for i in tutorial:
        print(i)"""
    if requested_url in tutorial:
        selected_url = Tutorial.objects.get(id=requested_url)
        print("Selected url ", selected_url.course_name)
        tutorial_related_urls = Tutorial.objects.filter(
            course_name__course_name=
            selected_url.course_name).order_by("tutorial_title")
        selected_url_index = list(tutorial_related_urls).index(selected_url)

        return render(request,
                      "tutor/tutorial.html",
                      {"tutorial":selected_url,
                      "sidebar":tutorial_related_urls,
                      "selected_url_index":selected_url_index})
    return HttpResponse(f"{requested_url} does not correspond to anything :(")

def search(request):
    query = request.GET.get('q')
    course_search_results = Course.objects.filter(Q(course_name__icontains=query))
    tutorial_search_result = Tutorial.objects.filter(Q(tutorial_title__icontains=query))
    tutorial_content_search_result = Tutorial.objects.filter(Q(tutorial_content__icontains=query))
    return render(request,
                  "tutor/search.html",
                  {"course_search_results":course_search_results,
                  'tutorial_search_results':tutorial_search_result,
                  'tutorial_content_search_results':tutorial_content_search_result})
   