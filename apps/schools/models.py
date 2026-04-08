from django.db import models


# -------------------------------
# School Model
# -------------------------------
class School(models.Model):
    abbreviation = models.CharField(
        max_length=12,
        blank=True,
        verbose_name="School Abbr"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="School Name",
        default="Unknown",
    )
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
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "1.1 List of Schools"
        ordering = ['name']


# -------------------------------
# Faculty Model
# -------------------------------
class Faculty(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='faculties'
    )
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "1.2 Faculties"
        ordering = ['last_name', 'first_name']


# -------------------------------
# Grade Level Model
# -------------------------------
class GradeLevel(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='grade_levels'
    )
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
    grade_level = models.ForeignKey(
        GradeLevel,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    name = models.CharField(max_length=100)
    adviser = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='advisory_sections'
    )
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
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='students'
    )
    student_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "1.5 Students"
        ordering = ['last_name', 'first_name']


# -------------------------------
# Enrollment Model
# -------------------------------
class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
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