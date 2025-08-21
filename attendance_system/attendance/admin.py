from django.contrib import admin
from .models import ClassRoom, Teacher, Student, TeacherAttendance, StudentAttendance, Complaint

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "classroom")
    list_filter = ("classroom",)
    search_fields = ("user__username", "subject")

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_number", "classroom")
    list_filter = ("classroom",)
    search_fields = ("user__username", "roll_number")

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ("teacher", "classroom", "date", "present", "timestamp")
    list_filter = ("classroom", "date", "present")
    search_fields = ("teacher__user__username",)

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "classroom", "date", "present", "marked_by_teacher", "timestamp")
    list_filter = ("classroom", "date", "present", "marked_by_teacher")
    search_fields = ("student__user__username", "student__roll_number")

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "resolved", "created_at")
    list_filter = ("resolved", "date")
    search_fields = ("student__user__username", "message")
