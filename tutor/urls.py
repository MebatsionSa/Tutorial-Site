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
    # path('search_results/q<slug:slug>/', views.SearchResults,name='search'),
    
]