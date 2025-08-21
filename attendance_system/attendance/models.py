from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ClassRoom(models.Model):
    """
    Example: name = "12th D"
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher")
    subject = models.CharField(max_length=100)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    roll_number = models.CharField(max_length=20, unique=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.roll_number})"


class TeacherAttendance(models.Model):
    """
    Auto-marked when teacher lands on teacher dashboard.
    One record per teacher per date.
    """
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    present = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("teacher", "date")

    def __str__(self):
        return f"{self.teacher.user.username} - {self.date} - {'Present' if self.present else 'Absent'}"


class StudentAttendance(models.Model):
    """
    Marked by teacher (class-wise). One record per student per date.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    present = models.BooleanField(default=False)
    marked_by_teacher = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "date")

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {'Present' if self.present else 'Absent'}"


class Complaint(models.Model):
    """
    Students can report issues for the day (or general).
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    message = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.student.user.username} on {self.date}"
