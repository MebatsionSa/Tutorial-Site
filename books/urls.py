from django.urls import path
from .import views
app_name = 'book'
urlpatterns = [
    path('index/',views.index,name='books-index'),
    path('',views.department,name='books-department'),
    path('<slug:requested_department>/',views.semester,name='books-semester'),
    path('<slug:requested_department>/<slug:selected_semester_courses>/',
    views.courses,name='books-courses'),
    path('<slug:requested_department>/<slug:selected_semester_courses>/<slug:selected_course_books>/',
    views.book,name='books-book'),
]
