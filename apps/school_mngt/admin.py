from django.contrib import admin
from django.utils.html import format_html
from .models import School, Faculty, GradeLevel, Section, Student, Enrollment


# =========================
# INLINE MODELS
# =========================
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
    fields = ('section', 'enrolled_date', 'is_active', 'notes')
    readonly_fields = ('enrolled_date',)
    autocomplete_fields = ['section']


# =========================
# SCHOOL ADMIN
# =========================
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'abbreviation',
        'founded_date',
        'colored_status',
        'faculty_count',
        'grade_level_count',
        'student_count',
        'logo_preview',
    )
    list_filter = ('status', 'founded_date')
    search_fields = ('name', 'abbreviation', 'tagline')
    ordering = ('name',)
    readonly_fields = ('logo_preview',)
    inlines = [GradeLevelInline]

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'abbreviation',
                'tagline',
                'founded_date',
                'status',
            )
        }),
        ('School Identity', {
            'fields': (
                'mission',
                'vision',
                'logo',
                'logo_preview',
            )
        }),
    )

    def colored_status(self, obj):
        color_map = {
            'pending': 'orange',
            'approved': 'green',
            'declined': 'red',
        }
        color = color_map.get(obj.status, 'black')
        return format_html(
            '<span style="font-weight:bold; color:{};">{}</span>',
            color,
            obj.get_status_display()
        )
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


# =========================
# FACULTY ADMIN
# =========================
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id',
        'full_name',
        'school',
        'email',
        'is_active',
        'advisory_count',
    )
    list_filter = ('school', 'is_active')
    search_fields = (
        'employee_id',
        'first_name',
        'last_name',
        'email',
        'school__name',
        'school__abbreviation',
    )
    ordering = ('last_name', 'first_name')
    autocomplete_fields = ['school']

    fieldsets = (
        ('Faculty Information', {
            'fields': (
                'school',
                'employee_id',
                'first_name',
                'last_name',
                'email',
                'is_active',
            )
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Faculty Name"

    def advisory_count(self, obj):
        return obj.advisory_sections.count()
    advisory_count.short_description = "Advisory Sections"


# =========================
# GRADE LEVEL ADMIN
# =========================
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


# =========================
# SECTION ADMIN
# =========================
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'grade_level',
        'school',
        'adviser',
        'capacity',
        'is_active',
        'student_count',
    )
    list_filter = ('is_active', 'grade_level__school', 'grade_level')
    search_fields = (
        'name',
        'grade_level__name',
        'grade_level__school__name',
        'adviser__first_name',
        'adviser__last_name',
    )
    ordering = ('grade_level__school', 'grade_level__order', 'name')
    autocomplete_fields = ['grade_level', 'adviser']

    fieldsets = (
        ('Section Information', {
            'fields': (
                'grade_level',
                'name',
                'adviser',
                'capacity',
                'is_active',
            )
        }),
    )

    def school(self, obj):
        return obj.grade_level.school
    school.short_description = "School"

    def student_count(self, obj):
        return obj.enrollments.count()
    student_count.short_description = "Enrolled Students"


# =========================
# STUDENT ADMIN
# =========================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'full_name',
        'school',
        'email',
        'enrollment_count',
    )
    list_filter = ('school',)
    search_fields = ('student_id', 'first_name', 'last_name', 'email', 'school__name')
    ordering = ('last_name', 'first_name')
    inlines = [EnrollmentInline]
    autocomplete_fields = ['school']

    fieldsets = (
        ('Student Information', {
            'fields': (
                'student_id',
                'school',
                'first_name',
                'last_name',
                'email',
            )
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Student Name"

    def enrollment_count(self, obj):
        return obj.enrollments.count()
    enrollment_count.short_description = "Enrollments"


# =========================
# ENROLLMENT ADMIN
# =========================
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'section',
        'school',
        'grade_level',
        'enrolled_date',
        'is_active',
    )
    list_filter = (
        'is_active',
        'section__grade_level__school',
        'section__grade_level',
        'section',
    )
    search_fields = (
        'student__student_id',
        'student__first_name',
        'student__last_name',
        'section__name',
        'section__grade_level__name',
    )
    ordering = ('-enrolled_date',)
    autocomplete_fields = ['student', 'section']

    fieldsets = (
        ('Enrollment Information', {
            'fields': (
                'student',
                'section',
                'enrolled_date',
                'is_active',
                'notes',
            )
        }),
    )
    readonly_fields = ('enrolled_date',)

    def school(self, obj):
        return obj.section.grade_level.school
    school.short_description = "School"

    def grade_level(self, obj):
        return obj.section.grade_level
    grade_level.short_description = "Grade Level"