from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from .models import School, Faculty, GradeLevel, Section, Student, Enrollment

User = get_user_model()

# -------------------------------
# INLINE MODELS
# -------------------------------
class GradeLevelInline(admin.TabularInline):
    model = GradeLevel
    extra = 1
    fields = ('name', 'order')


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    fields = ('name', 'adviser', 'capacity', 'is_active')
    autocomplete_fields = ['adviser']


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    fields = ('student', 'enrolled_date', 'is_active', 'notes')
    readonly_fields = ('enrolled_date',)
    autocomplete_fields = ['student', 'section']


# -------------------------------
# SCHOOL ADMIN
# -------------------------------
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'abbreviation',
        'colored_status',
        'faculty_count',
        'grade_level_count',
        'student_count',
        'logo_preview',
    )
    list_filter = ('status',)
    search_fields = ('name', 'abbreviation', 'tagline')
    readonly_fields = ('logo_preview',)
    inlines = [GradeLevelInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'abbreviation', 'tagline', 'founded_date', 'status')
        }),
        ('School Identity', {
            'fields': ('mission', 'vision', 'logo', 'logo_preview')
        }),
    )

    def colored_status(self, obj):
        color_map = {
            'pending': 'orange',
            'approved': 'green',
            'declined': 'red',
        }
        color = color_map.get(obj.status, 'black')
        return format_html('<span style="font-weight:bold; color:{};">{}</span>',
                           color, obj.get_status_display())
    colored_status.short_description = "Status"

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:contain; border-radius:8px;" />',
                obj.logo.url
            )
        return "No Logo"
    logo_preview.short_description = "Logo"

    def faculty_count(self, obj):
        return obj.faculties.count()
    faculty_count.short_description = "Faculties"

    def grade_level_count(self, obj):
        return obj.grade_levels.count()
    grade_level_count.short_description = "Grade Levels"

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Students"

from django.contrib import admin
from .models import School, Faculty, GradeLevel, Section, Student, Enrollment

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'school', 'is_active')
    list_filter = ('school', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    autocomplete_fields = ('user', 'school')

    def full_name(self, obj):
        if obj.user:  # check if user exists
            return obj.user.get_full_name() or obj.user.username
        return "No user assigned"
    full_name.short_description = "Faculty Name"    

# -------------------------------
# GRADE LEVEL ADMIN
# -------------------------------
@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'order', 'section_count')
    list_filter = ('school',)
    search_fields = ('name', 'school__name', 'school__abbreviation')
    ordering = ('school', 'order', 'name')
    inlines = [SectionInline]
    autocomplete_fields = ['school']

    def section_count(self, obj):
        return obj.sections.count()
    section_count.short_description = "Sections"


# -------------------------------
# SECTION ADMIN
# -------------------------------
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'school', 'adviser_name', 'capacity', 'is_active', 'student_count')
    list_filter = ('is_active', 'grade_level__school', 'grade_level')
    search_fields = (
        'name',
        'grade_level__name',
        'grade_level__school__name',
        'adviser__user__first_name',
        'adviser__user__last_name',
    )
    ordering = ('grade_level__school', 'grade_level__order', 'name')
    autocomplete_fields = ['grade_level', 'adviser']

    def school(self, obj):
        return obj.grade_level.school
    school.short_description = "School"

    def adviser_name(self, obj):
        if obj.adviser:
            return obj.adviser.user.get_full_name() or obj.adviser.user.username
        return "-"
    adviser_name.short_description = "Adviser"

    def student_count(self, obj):
        return obj.enrollments.count()
    student_count.short_description = "Enrolled Students"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'school')
    list_filter = ('school',)
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    autocomplete_fields = ('user', 'school')

    def full_name(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return "No user assigned"
    full_name.short_description = "Student Name"

# -------------------------------
# ENROLLMENT ADMIN
# -------------------------------
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'section', 'school', 'grade_level', 'enrolled_date', 'is_active')
    list_filter = ('is_active', 'section__grade_level__school', 'section__grade_level', 'section')
    search_fields = (
        'student__user__first_name',
        'student__user__last_name',
        'student__user__username',
        'section__name',
        'section__grade_level__name',
    )
    ordering = ('-enrolled_date',)
    autocomplete_fields = ['student', 'section']
    readonly_fields = ('enrolled_date',)

    def student_name(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    student_name.short_description = "Student"

    def school(self, obj):
        return obj.section.grade_level.school
    school.short_description = "School"

    def grade_level(self, obj):
        return obj.section.grade_level
    grade_level.short_description = "Grade Level"