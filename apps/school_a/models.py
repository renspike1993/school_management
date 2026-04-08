from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# -------------------------------
# School Model
# -------------------------------
class School(models.Model):
    abbreviation = models.CharField(max_length=12, blank=True, verbose_name="School Abbr")
    name = models.CharField(max_length=255, verbose_name="School Name", default="Unknown")
    tagline = models.CharField(max_length=500, blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    founded_date = models.DateField()

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Approval Status")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "1.1 List of Schools"
        ordering = ['name']


# -------------------------------
# Faculty Model (Instructor)
# -------------------------------
class Faculty(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='faculties')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='faculty_profile',  # unique for Faculty
        null=True,   # temporary for existing rows
        blank=False
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.user:
            return f"{self.user.get_full_name() or self.user.username}"
        return "Unknown Faculty"

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "1.2 Faculties"
        ordering = ['user__last_name', 'user__first_name']


# -------------------------------
# Grade Level Model
# -------------------------------
class GradeLevel(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='grade_levels')
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.school.abbreviation or self.school.name}"

    class Meta:
        verbose_name = "Grade Level"
        verbose_name_plural = "1.3 Grade Levels"
        unique_together = ('school', 'name')
        ordering = ['order', 'name']


# -------------------------------
# Section Model
# -------------------------------
class Section(models.Model):
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100)
    adviser = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='advisory_sections')
    capacity = models.PositiveSmallIntegerField(default=40)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.grade_level.name} - {self.name}"

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "1.4 Sections"
        unique_together = ('grade_level', 'name')
        ordering = ['grade_level__order', 'grade_level__name', 'name']


# -------------------------------
# Student Model
# -------------------------------
class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',  # unique for Student
        null=True,  # temporary for existing rows
        blank=False
    )

    def __str__(self):
        if self.user:
            return f"{self.user.get_full_name() or self.user.username}"
        return "Unknown Student"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "1.5 Students"
        ordering = ['user__last_name', 'user__first_name']


# -------------------------------
# Enrollment Model
# -------------------------------
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.section}"

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "1.6 Enrollments"
        unique_together = ('student', 'section')
        ordering = ['-enrolled_date']