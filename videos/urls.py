from django.urls import path
from . import views

app_main = 'video'
urlpatterns = [
    path('index/',views.index,name='video-index'),
    path('',views.home,name='videos-home'),
    path('<slug:selected_department>/',views.courses,name='videos-courses'),
    path('<slug:selected_department>/<slug:selected_course>/<int:selected_video>/',
    views.videos,name='videos-video'),
]