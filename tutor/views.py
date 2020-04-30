from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, Course, Department
from authentication.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
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
    department = [d.department_short_name for d in Department.objects.all()]
    print(department)
    print("El departmente finished #########")
    if requested_department in department:
        matching_course = Course.objects.filter(
            department_name__department_short_name=requested_department)
        for i in matching_course:
            print(i)
        tutorial_urls={} # all tutorials found in requested department
        for each in matching_course.all():
            print(each.course_code)
            tutorials = Tutorial.objects.filter(
                course_code__course_code=each.course_code).earliest('pub_date')
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
    toot = Tutorial.objects.get(id=requested_url)
    """print(toot.course_code.id,type(toot))
    print(requested_department, type(requested_url))"""
    tut = get_object_or_404(Tutorial, 
    id=requested_url,
    course_code=toot.course_code.id,
    course_code__department_name=toot.course_code.department_name.id)
    # print("After ",requested_department, requested_url)
    print(tut.id, tut.course_code.id)
    is_liked = False
    if tut.likes.filter(id=request.user.id).exists():
        is_liked = True

    department = [d.department_name for d in Department.objects.all()]
    if requested_department in department:
        matching_course = Course.objects.filter(
            department_name__department_short_name=requested_department)

        tutorial_urls={} # all tutorials found in requested department
        for each in matching_course.all():
            tutorials = Tutorial.objects.filter(
                course_code__course_code=each.course_name).earliest('pub_date')
            
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
        # selected_url = selected_url.course_code
        print("Selected url ", selected_url)
        tutorial_related_urls = Tutorial.objects.filter(
            course_code=selected_url.course_code).order_by("tutorial_title")
        selected_url_index = list(tutorial_related_urls).index(selected_url)
        who = tut.who_liked()
        current_year=timezone.now().year
        # who_likes = who.filter(likes__pub_date__year=current_year)[:2]
        who_likes = who.order_by('-last_login')[:2]
        who_ = ', '.join([u.username for u in who_likes])
        print(who_likes.count())
        print(is_liked)
        # for i in who:
          #  print(i)
        return render(request,
                      "tutor/tutorial.html",
                      {"tutorial":selected_url,
                      "sidebar":tutorial_related_urls,
                      "selected_url_index":selected_url_index,
                      "tut":tut,
                      "is_liked":is_liked,
                      "total_likes":tut.total_likes(),
                      "who":who_
                      })
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
 
def like_post(request,num):
    tut = get_object_or_404(Tutorial, id=request.POST.get('tutorial_id'))
    user=[]
    is_liked = False
    if tut.likes.filter(id=request.user.id).exists():
        print("tut ",tut)
        tut.likes.remove(request.user)
        print(request.user)
        is_liked = False
    else:
        tut.likes.add(request.user)
        user.append(request.user)
        is_liked = True
    return HttpResponseRedirect(tut.get_absolute_url())

