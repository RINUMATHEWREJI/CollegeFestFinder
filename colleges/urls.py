from django.urls import path
from . import views

app_name = 'colleges'

urlpatterns = [
    path('colleges_login/', views.colleges_login, name='colleges_login'),
    path('colleges_signup/', views.colleges_signup, name='colleges_signup'),
    path('college_homepage/', views.college_homepage, name='college_homepage'),
    path('add_event/', views.add_event, name='add_event'),
    path('delete_event/', views.delete_event_page, name='delete_event_page_without_id'),
    path('delete_event/<int:event_id>/', views.delete_event_page, name='delete_event'),
    path('update_event_page/', views.update_event_page, name='update_event_page'),
    path('update_event/<int:event_id>/', views.update_event, name='update_event'),
    path('colleges_logout/',views.colleges_logout, name='colleges_logout'),

]
