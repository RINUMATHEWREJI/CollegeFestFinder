from django.urls import path
from . import views

urlpatterns = [
 path('colleges_login/',views.colleges_login,name='colleges_login'),
 path('colleges_signup/',views.colleges_signup,name='colleges_signup'),  
 path('college_homepage/',views.college_homepage,name='college_homepage'), 
]