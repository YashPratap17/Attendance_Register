from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import (
    ClassRoom, Teacher, Student,
    TeacherAttendance, StudentAttendance, Complaint
)
from .forms import ComplaintForm

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    # Redirect based on role
    if request.user.is_superuser:
        return redirect("admin_dashboard")
    if hasattr(request.user, "teacher"):
        return redirect("teacher_dashboard")
    if hasattr(request.user, "student"):
        return redirect("student_dashboard")
    # If user has no role object, send to login
    return redirect("login")

@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, "teacher"):
        return HttpResponseForbidden("Only teachers can view this page.")
    teacher = request.user.teacher
    today = timezone.localdate()

    # Auto-mark teacher check-in (once per day)
    checkin, _created = TeacherAttendance.objects.get_or_create(
        teacher=teacher,
        date=today,
        defaults={"classroom": teacher.classroom, "present": True},
    )

    # Has the teacher marked class attendance today?
    class_marked_today = StudentAttendance.objects.filter(
        classroom=teacher.classroom,
        date=today,
        marked_by_teacher=True
    ).exists()

    return render(request, "attendance/teacher_dashboard.html", {
        "teacher": teacher,
        "teacher_checkin": checkin,
        "class_marked_today": class_marked_today,
    })

@login_required
def mark_class_attendance(request):
    if not hasattr(request.user, "teacher"):
        return HttpResponseForbidden("Only teachers can mark attendance.")
    teacher = request.user.teacher
    today = timezone.localdate()
    students = Student.objects.filter(classroom=teacher.classroom).select_related("user")

    if request.method == "POST":
        for s in students:
            present = request.POST.get(f"present_{s.id}") == "on"
            StudentAttendance.objects.update_or_create(
                student=s,
                date=today,
                defaults={
                    "classroom": teacher.classroom,
                    "present": present,
                    "marked_by_teacher": True
                }
            )
        return redirect("teacher_dashboard")

    return render(request, "attendance/mark_class_attendance.html", {
        "teacher": teacher,
        "students": students
    })

@login_required
def student_dashboard(request):
    if not hasattr(request.user, "student"):
        return HttpResponseForbidden("Only students can view this page.")
    student = request.user.student

    records = StudentAttendance.objects.filter(student=student).order_by("-date")
    total_days = records.count()
    present_days = records.filter(present=True).count()
    attendance_percentage = round((present_days / total_days) * 100, 2) if total_days else 0.0

    # Complaint form
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.student = student
            comp.date = timezone.localdate()
            comp.save()
            return redirect("student_dashboard")
    else:
        form = ComplaintForm()

    complaints = Complaint.objects.filter(student=student).order_by("-created_at")

    return render(request, "attendance/student_dashboard.html", {
        "student": student,
        "attendance_records": records,
        "attendance_percentage": attendance_percentage,
        "complaints": complaints,
        "form": form
    })

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    today = timezone.localdate()
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    teachers_checked_in_today = TeacherAttendance.objects.filter(date=today, present=True).count()
    classes_marked_today = StudentAttendance.objects.filter(date=today, marked_by_teacher=True).values("classroom").distinct().count()
    recent_complaints = Complaint.objects.select_related("student__user").order_by("-created_at")[:10]

    return render(request, "attendance/admin_dashboard.html", {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "teachers_checked_in_today": teachers_checked_in_today,
        "classes_marked_today": classes_marked_today,
        "recent_complaints": recent_complaints,
        "today": today
    })


