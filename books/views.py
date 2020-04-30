from django.shortcuts import render
from django.http import HttpResponse
from .models import Department, Semester, Course, Book
# Create your views here.

def index(request):
    return HttpResponse('This is Book index')

def department(request):
    d = Department.objects.all()
    for i in d:
        print(i.department_short_name)
    return render(request=request,
                  template_name="books/departments.html",
                  context={"department":d}
                )

def semester(request,requested_department):
    department = [d.department_short_name for d in Department.objects.all()]
    if requested_department in department:
        all_semester_entered = Semester.objects.filter(
            department_id__department_short_name=requested_department)
    for i in all_semester_entered:
        print(i)
    
    return render(request,
                  "books/semester.html",
                  {"all_semester":all_semester_entered}
                )

def courses(request, requested_department, selected_semester_courses):
    department = [d.department_short_name for d in Department.objects.all()]
    if requested_department in department:
        all_semester_entered = Semester.objects.filter(
            department_id__department_short_name=requested_department)
        department_semesters = [s.semester_name for s in Semester.objects.all()]
        print([i for i in department_semesters])
        if selected_semester_courses: # in department_semesters:
            course_for_semester = Course.objects.filter(
                semester_name__semester_name=selected_semester_courses
            )
            
            courses = [j for j in course_for_semester]
            print("courses ",courses)
            bookstore = {}
            for _of_the_course in courses:
                print("The course ",_of_the_course)
                books_for_course = Book.objects.filter(course_code_id__course_name=_of_the_course)
                for each_book in books_for_course:
                    p = each_book.book_name
                    print("book ",p)
                    bookstore[_of_the_course] = p 
            # print(type(books))
                print([b.book_name for b in books_for_course])
            """
            for v, k in bookstore.items:
                print(v.semester_name, "###",k.book_name)
                """
            print(type(bookstore.items))
            for k, v in bookstore.items():
                print(k, "****",v)
        else:
            return HttpResponse("The selected semester have no courses")
    else:
        print("The required department don't exist.")
    return render(request,
                  "books/courses.html",
                  {"courses":courses,
                   "books":bookstore}
                )

def book(request,requested_department, selected_semester_courses,selected_course_books):
    department = [d.department_short_name for d in Department.objects.all()]
    if requested_department in department:
        all_semester_entered = Semester.objects.filter(
            department_id__department_short_name=requested_department)
        department_semesters = [s.semester_name for s in Semester.objects.all()]
        print([i for i in department_semesters])
        if selected_semester_courses: # in department_semesters:
            course_for_semester = Course.objects.filter(
                semester_name__semester_name=selected_semester_courses
            )
            
            # courses = [j for j in course_for_semester]
            courses = [type(j.id) for j in course_for_semester]
            print("courses ",courses)
            print(type(selected_course_books))
            selected_course_books = int(selected_course_books)
            print(type(selected_course_books))
            if selected_course_books:
                print("Here")
                all_selected_course_books = Book.objects.filter(
                    course_code_id__id=selected_course_books
                )
            for i in all_selected_course_books:
                print(i.book_name)

        else:
            return HttpResponse("The selected semester have no courses")
    else:
        print("The required department don't exist.")
    return render(request,
                  "books/books.html",
                  {"books":all_selected_course_books}
                )

