from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # STUDENTS
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:id>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:id>/', views.student_delete, name='student_delete'),

    # CLASSES
    path('classes/', views.class_list, name='class_list'),
    path('classes/add/', views.class_add, name='class_add'),
    path('classes/edit/<int:id>/', views.class_edit, name='class_edit'),
    path('classes/delete/<int:id>/', views.class_delete, name='class_delete'),

    # DIVISIONS
    path('divisions/', views.division_list, name='division_list'),
    path('divisions/add/', views.division_add, name='division_add'),
    path('divisions/edit/<int:id>/', views.division_edit, name='division_edit'),
    path('divisions/delete/<int:id>/', views.division_delete, name='division_delete'),
]
