 
def like_post(request,requested_department, course_name, requested_url):
    print(requested_department,course_name,requested_url)  # requested_department, course_name, requested_url
    #  requested_department=tutorial.course_code.department_name 
    # course_name=tutorial.course_code 
    requested_url=tutorial.id
    print(request.POST.get('id'))
    tut = get_object_or_404(Tutorial, id=request.POST.get('id'))
    print(request.POST.get('id'))
    tut.likes.add(request.user)
    return HttpResponseRedirect(tut.get_absolute_url())

path('<slug:requested_department>/<slug:course_name>/<int:requested_url>/',views.like_post,name='like_post'),

<form action="{% url 'tutor:like_post'  requested_department=tutorial.course_code.department_name course_name=tutorial.course_code requested_url=tutorial.id %}" method="POST">
                {% csrf_token %}
                <button type="submit" name="id" value="{{id}}" class="btn waves-effect waves-light" 
                style="background-color: royalblue;">Like</button>
            </form>


def like_detail(request, requested_department, course_name, requested_url, slug):
    toot = Tutorial.objects.get(id=requested_url)
    print(toot.course_code.id,type(toot))
    print(requested_department, type(requested_url))
    tut = get_object_or_404(Tutorial, slug=slug, id=requested_url,course_code=toot.course_code.id,course_code__department_name=toot.course_code.department_name.id)
    print("After ",requested_department, requested_url)
    is_liked = False
    if tut.likes.filter(id=request.user.id).exists():
        tut.likes.remove(request.user)
        print(course_name)
        is_liked = False
    else:
        tut.likes.add(request.user)
        is_liked = True

            {# comment #}
            <!-- <form action="{% url 'tutor:like_post'  requested_department=tutorial.course_code.department_name course_name=tutorial.course_code requested_url=tutorial.id %}" method="POST">
                {% csrf_token %}
                <button type="submit" name="id" value="{{id}}" class="btn waves-effect waves-light" 
                style="background-color: royalblue;">Like</button>
            </form> -->
        {# endcomment #}
   {% if is_liked %}
                    <button type="submit" name="tutorial_id" value="{{tut.id}}" class="btn waves-effect waves-light" 
                    style="background-color: rgb(239, 31, 31);">Dislike</button>
                {% else %}

                <!--{# comment #}
                    
                    {% else %}
                        <button type="submit" name="tutorial_id" value="{{tut.id}}" class="btn waves-effect waves-light" 
                        style="background-color: royalblue;">Like</button>
                    {% endif %}
                {# endcomment #} -->

tutorial.html
            {{total_likes}} Like{{total_likes|pluralize}}<br>
            {{who}} like this tutorial.
            <!-- {{tut.get_absolute_url}} -->
            <form action="{% url 'tutor:like_post' tut.id %}" method="POST">
                {% csrf_token %}
                {% if is_liked %}
                    <button type="submit" name="tutorial_id" value="{{tut.id}}" class="btn waves-effect waves-light" 
                    style="background-color: rgb(239, 31, 31);">Dislike</button>
                {% else %}
                    <button type="submit" name="tutorial_id" value="{{tut.id}}" class="btn waves-effect waves-light" 
                    style="background-color: royalblue;">Like</button>
                {% endif %}
            </form>
views.py
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

urls.py
    from django.urls import path
    from .import views
    from tutor import views
    app_name = 'tutor'
    urlpatterns = [
        path('',views.home,name='home'),
        path('search/',views.search,name='search'),
        path('<slug:requested_department>/',views.course,name='course'),
        path('<slug:requested_department>/<slug:course_name>/<int:requested_url>/', 
        views.tutorial,name='tutorial'),
        path('likes/<int:num>',views.like_post,name='like_post'),
        # path('search_results/q<slug:slug>/', views.SearchResults,name='search'),
        # <slug:requested_department>/<slug:course_name>/<int:requested_url>/<int:id>
    ]

def login_(request):
    if request.user.is_authenticated:
        username = form.cleaned_data.get('')
        return redirect("tutor:home")
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                print("Velcome ")
                if user is not None:
                    form = login(request,user)
                    print("Velcome ")
                    messages.success(request, f"you are now logged in as {username}")
                    print("Velcome ")
                    redirect("authentication:login")
                    return redirect("tutor:home")
                    messages.success(request, f"you are now logged in as {username}")

                    print("Velcome ")
                else:
                    messages.error(request, "Invalid username or password due something wrong with {username}'s account.")

            else:
                # messages.error(request, "Invalid username or password")
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = User.objects.get(username=username)
                if user is not None:
                    login(request, user)
                    return redirect("tutor:home")
                else:
                    messages.error(request, "The user is not registered yet.")                

    form = AuthenticationForm()
    return render(request,
                  "authentication/login.html",
                  {'form':form})

# anonymous user
def login_(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if request.user.is_anonymous:
            print()
            error = list(form.error_messages.values())
            p = str(error[0])
            print(p)
            print(messages.error(request, p))

        else:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                print("Velcome ")
                if user is not None:
                    form = login(request,user)
                    print("Velcome ")
                    messages.success(request, f"you are now logged in as {username}")
                    print("Velcome ")
                    return redirect("tutor:home")
                    messages.success(request, f"you are now logged in as {username}")

                    print("Velcome ")
                else:
                    messages.error(request, "Invalid username or password due something wrong with {username}'s account.")

            else:
                messages.error(request, "Invalid username or password")
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                messages.error(request, "Invalid username or password")
        
                user = User.objects.get(username=username)
                if user is not is_anonymous:
                    login(request, user)
                    messages.success(request, f"you are now logged in as {username}")                 
                    return redirect("tutor:home")
                else:
                    messages.error(request, "The user is not registered yet.")                
    
    form = AuthenticationForm()
    return render(request,
                  "authentication/login.html",
                  {'form':form}) 

#previously
def login_(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print("Velcome ")
            if user is not None:
               form = login(request,user)
               print("Velcome ")
               messages.success(request, f"you are now logged in as {username}")
               print("Velcome ")
               return redirect("tutor:home")
               messages.success(request, f"you are now logged in as {username}")

               print("Velcome ")
            else:
                messages.error(request, "Invalid username or password due something wrong with {username}'s account.")

        else:
            messages.error(request, "Invalid username or password")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = User.objects.get(username=username)
            if user is not None:
                login(request, user)
                messages.success(request, f"you are now logged in as {username}")                 
                return redirect("tutor:home")
            else:
                messages.error(request, "The user is not registered yet.")                

    form = AuthenticationForm()
    return render(request,
                  "authentication/login.html",
                  {'form':form})

# latest but says anonymous for all users
def login_(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if request.user.is_anonymous:
            messages.info(request, "Please enter a correct %s and password." % ('username'))
            messages.info(request, "Note that both fields may be case-sensitive.")
            return redirect("authentication:login")
            """print()
            error = list(form.error_messages.values())
            p = str(error[0])
            print(p)
            print(messages.error(request, p))"""

        else:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                print("Velcome ")
                if user is not None:
                    form = login(request,user)
                    print("Velcome ")
                    messages.success(request, f"you are now logged in as {username}")
                    print("Velcome ")
                    return redirect("tutor:home")
                    messages.success(request, f"you are now logged in as {username}")

                    print("Velcome ")
                else:
                    messages.error(request, "Invalid username or password due something wrong with {username}'s account.")

            else:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                messages.info(request, "Invalid username or password")
        
                user = User.objects.get(username=username)
                if user is not is_anonymous:
                    login(request, user)
                    messages.success(request, f"you are now logged in as {username}")                 
                    return redirect("tutor:home")
                else:
                    messages.error(request, "The user is not registered yet.")                
    
    form = AuthenticationForm()
    return render(request,
                  "authentication/login.html",
                  {'form':form}) 

# before get_user_model()