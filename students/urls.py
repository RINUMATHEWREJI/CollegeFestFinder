from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login_selection/',views.login_selection,name='login_selection'),


    path('student_login/',views.student_login,name='student_login'),
    path('student_signup/',views.student_signup,name='student_signup'),
    path('student_homepage/',views.student_homepage,name='student_homepage'),
    path('college/<int:college_id>/', views.view_college_events, name='view_college_events'),
    path('register_event/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('student_logout/',views.student_logout,name='student_logout'),
]