from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login_selection/',views.login_selection,name='login_selection'),


    path('student_login/',views.student_login,name='student_login'),
    path('student_signup/',views.student_signup,name='student_signup'),
    path('student_homepage/',views.student_homepage,name='student_homepage'),
]