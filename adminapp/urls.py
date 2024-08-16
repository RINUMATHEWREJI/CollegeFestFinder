from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_signup/',views.admin_signup,name='admin_signup'),
    path('admin_homepage/',views.admin_homepage,name='admin_homepage'),
]