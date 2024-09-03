from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('add_admin/',views.add_admin,name='add_admin'),
    path('admin_homepage/',views.admin_homepage,name='admin_homepage'),
    path('edit_events_page/<int:college_id>',views.edit_events_page,name='edit_events_page'),
    path('edit_events/<int:event_id>',views.edit_events,name='edit_events'),
    path('delete_events/<int:event_id>',views.delete_events,name='delete_events'),
    path('manage_students/',views.manage_students,name='manage_students'),
    path('edit_student/<int:student_id>',views.edit_student,name = 'edit_student'),
    path('delete_student/<int:student_id>',views.delete_student,name='delete_student'),
    path('add_student/',views.add_student,name = 'add_student'),
]