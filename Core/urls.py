from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashbord, name='dashbord'),
    path('centers/', views.center_list, name='center_list'),
    path('centers/add/', views.center_add, name='center_add'),
    path('centers/<int:center_id>/edit/', views.center_edit, name='center_edit'),
    path('centers/<int:center_id>/delete/', views.center_delete, name='center_delete'),

    path('center_student_list/<int:center_id>/', views.center_student_list, name='center_student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('add_student_tow', views.add_student_tow, name='add_student_tow'),
    path('student_list', views.student_list, name='student_list'),
    path('update-student/<int:student_id>/', views.update_student, name='update_students'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),

    path('login', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    

    path('coordinators/', views.coordinator_list, name='coordinator_lists'),
    path('add_coordinator/', views.add_coordinator, name='add_coordinator'),
    path('coordinator/<int:coordinator_id>/edit/', views.edit_coordinator, name='edit_coordinator'),
    path('delete-coordinator/<int:coordinator_id>/', views.delete_coordinator, name='delete_coordinator'),


]
