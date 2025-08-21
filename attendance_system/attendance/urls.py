from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Teacher
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/mark/", views.mark_class_attendance, name="mark_class_attendance"),

    # Student
    path("student/", views.student_dashboard, name="student_dashboard"),

    # Superuser
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
