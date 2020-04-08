from django.urls import include, path
from .import views
app_name = "authentication"
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login_,name='login'),
    path('logout/',views.logout_,name='logout'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]