from django.contrib import admin
# from django.urls import reverse
# from django.utils.html import format_html
# from django.utils.safestring import mark_safe
# from django.db.models import Count, Sum
# from decimal import Decimal

# # Unfold imports
from unfold.admin import ModelAdmin, TabularInline,StackedInline
from .models import School,Curriculum
# from .models import (
#     School, GradeSection, Subject, Instructor, Student,
#     Enrollment, Assignment, Schedule, Payment, TuitionFee
# )


# # ---------- Inlines ----------
# class EnrollmentInline(TabularInline):
#     model = Enrollment
#     extra = 1
#     fields = ['student', 'created_at']
#     readonly_fields = ['created_at']
#     autocomplete_fields = ['student']


# class PaymentInline(TabularInline):
#     model = Payment
#     extra = 0
#     fields = ['amount', 'payment_date', 'due_date', 'status', 'payment_method', 'reference_number']
#     readonly_fields = ['payment_date']
#     autocomplete_fields = ['parent_payment']
#     classes = ['collapse']


# class ScheduleInline(TabularInline):
#     model = Schedule
#     extra = 1
#     fields = ['time_started', 'time_ended', 'frequency_date']


from django.utils.html import format_html
from .models import School,Curriculum,Program,Books,Subject,Syllabus

from django.contrib import admin
from django.utils.html import format_html
from .models import School

@admin.register(School)
class SchoolAdmin(ModelAdmin):
    list_display = [ 'display_logo','school_name','abbrevation', 'tagline', 'started_at', 'colored_status',]
    list_filter = ['started_at', 'status']
    search_fields = ['school_name', 'abbrevation', 'tagline', 'mission', 'vision']
    readonly_fields = ['display_logo_preview']

    fieldsets = (
        ('Basic Information', {
            'fields': ('abbrevation', 'school_name', 'tagline',  'started_at')
        }),
        ('Requirements', {
            'fields': ('status',)
        }),


        ('Logo', {
            'fields': ('logo', 'display_logo_preview')
        }),
        
        
        ('About', {
            'fields': ('mission', 'vision'),
            'classes': ('wide',)
        }),
    )

    # ----- Logo functions -----
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:5px;" />', obj.logo.url)
        return "No Logo"


    def display_logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="150" style="border-radius:8px;" />', obj.logo.url)
        return "No Logo Uploaded"
    
    # ----- Colored Status with Tailwind -----
    def colored_status(self, obj):
        color_map = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'approved': 'bg-green-100 text-green-800',
            'declined': 'bg-red-100 text-red-800',
        }
        
        classes = color_map.get(obj.status, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 rounded-full text-sm font-semibold {}">{}</span>',
            classes,
            obj.get_status_display()
        )
    def status(self):
        return format_html('<input type="checkbox">')
        
    display_logo.short_description = "Logo"
    display_logo_preview.short_description = "Logo Preview"
    status.short_description = "status"
    colored_status.short_description = "Status"
    colored_status.admin_order_field = 'status'
from apps.cmo.models import ChedOrders
# =====================
# Curriculum Inline
# =====================


class SubjectInline(TabularInline):
    model = Subject
    extra = 1  # Number of empty rows for adding new curriculums
    fields = ('subject_code', 'subject_description')
    autocomplete_fields = ['subject']  # optional for large lists
    show_change_link = True
    
class CurriculumInline(TabularInline):
    model = Curriculum
    extra = 1  # Number of empty rows for adding new curriculums
    fields = ('program', 'started_at')
    autocomplete_fields = ['program']  # optional for large lists
    show_change_link = True

class ChedOrdersInline(TabularInline):
    model = ChedOrders
    extra = 1  # Number of empty rows for adding new curriculums
    fields = ('compliance_category')
    show_change_link = True

class BookInline(TabularInline):
    model = Books
    extra = 1  # Number of empty rows for adding new curriculums
    fields = ('title','author','collection',)

    show_change_link = True




# class ChedOrdersInline(TabularInline):
#     model = ChedOrders
#     extra = 1  # Number of empty rows for adding new curriculums
#     fields = ('ra_num','description',)

#     show_change_link = True
# =====================
# Program Admin
# =====================
@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    list_display = ( 'program_name', 'major','colored_status',)
    list_filter = ('started_at',)
    search_fields = ('program_name', 'abbreviation',)
    inlines = [CurriculumInline]  # Show curriculums inside Program

    def colored_status(self, obj):
            color_map = {
                'pending': 'bg-yellow-100 text-yellow-800',
                'approved': 'bg-green-100 text-green-800',
                'declined': 'bg-red-100 text-red-800',
            }
            
            classes = color_map.get(obj.status, 'bg-gray-100 text-gray-800')
            return format_html(
                '<span class="px-2 py-1 rounded-full text-sm font-semibold {}">{}</span>',
                classes,
                obj.get_status_display()
            )

@admin.register(Curriculum)
class CurriculumAdmin(ModelAdmin):
    list_display = ['curriculum_name','colored_status', 'program',]
    list_filter = ['started_at',]
    search_fields = ( 'curriculum_name',) 
    def colored_status(self, obj):
                color_map = {
                    'pending': 'bg-yellow-100 text-yellow-800',
                    'approved': 'bg-green-100 text-green-800',
                    'declined': 'bg-red-100 text-red-800',
                }
                
                classes = color_map.get(obj.status, 'bg-gray-100 text-gray-800')
                return format_html(
                    '<span class="px-2 py-1 rounded-full text-sm font-semibold {}">{}</span>',
                    classes,
                    obj.get_status_display()
                )

@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = [ 'subject_code','subject_desc','subject_unit','unit_group']
    list_filter = ['subject_desc']
    search_fields = ('subject_desc',)
    fields = ('subject_code','subject_desc','unit_group','subject_unit',)
    inlines = [BookInline]
    
@admin.register(Books)
class BookAdmin(ModelAdmin):
    list_display = [ 'title','author','collection',]
    list_filter = ['title',]
    search_fields = ('title',)

@admin.register(Syllabus)
class SyllabusAdmin(ModelAdmin):
    list_display = [ 'subject','curriculum__program__program_name',]
    list_filter = ['subject',]
    search_fields = ('subject',)



# # ---------- GradeSection ----------
# @admin.register(GradeSection)
# class GradeSectionAdmin(ModelAdmin):
#     list_display = ['section_name', 'grade', 'school', 'student_count', 'assignment_count', 'enrollment_count', 'subjects_list']
#     list_filter = ['school', 'grade']
#     search_fields = ['section_name', 'school__school_name']
#     list_editable = ['grade']
#     inlines = [EnrollmentInline]
#     autocomplete_fields = ['school']
#     readonly_fields = ['student_count_display', 'assignment_count_display', 'enrollment_count_display', 'subjects_detailed']

#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('school', 'section_name', 'grade')
#         }),
#         ('Statistics', {
#             'fields': ('student_count_display', 'assignment_count_display', 'enrollment_count_display', 'subjects_detailed'),
#             'classes': ('wide',)
#         }),
#     )

#     def get_queryset(self, request):
#         return super().get_queryset(request).annotate(
#             student_count=Count('enrollments__student', distinct=True),
#             assignment_count=Count('assignments', distinct=True)
#         )

#     def student_count(self, obj):
#         if hasattr(obj, 'student_count'):
#             return obj.student_count
#         return obj.enrollments.values('student').distinct().count()
#     student_count.short_description = 'Students'
#     student_count.admin_order_field = 'student_count'

#     def student_count_display(self, obj):
#         count = self.student_count(obj)
#         return format_html('<span style="font-weight: bold; color: #17a2b8;">{} Students</span>', count)
#     student_count_display.short_description = 'Students'

#     def assignment_count(self, obj):
#         if hasattr(obj, 'assignment_count'):
#             return obj.assignment_count
#         return obj.assignments.count()
#     assignment_count.short_description = 'Assignments'
#     assignment_count.admin_order_field = 'assignment_count'

#     def assignment_count_display(self, obj):
#         count = self.assignment_count(obj)
#         return format_html('<span style="font-weight: bold; color: #ffc107;">{} Assignments</span>', count)
#     assignment_count_display.short_description = 'Assignments'

#     def enrollment_count(self, obj):
#         return obj.enrollments.count()
#     enrollment_count.short_description = 'Enrollments'

#     def enrollment_count_display(self, obj):
#         count = obj.enrollments.count()
#         return format_html('<span style="font-weight: bold; color: #28a745;">{} Enrollments</span>', count)
#     enrollment_count_display.short_description = 'Enrollments'

#     def subjects_list(self, obj):
#         subjects = Subject.objects.filter(assignments__grade_section=obj).distinct()
#         if not subjects:
#             return "No subjects assigned"
#         subject_names = [f"{subject.code}" for subject in subjects[:3]]
#         result = ", ".join(subject_names)
#         if subjects.count() > 3:
#             result += f" and {subjects.count() - 3} more"
#         return result
#     subjects_list.short_description = 'Subjects'

#     def subjects_detailed(self, obj):
#         assignments = obj.assignments.all().select_related('subject', 'instructor')
#         if not assignments:
#             return "No subjects assigned to this grade section"

#         html = '<div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">'
#         html += '<h4>Subjects Offered</h4>'
#         html += '<table style="width: 100%; border-collapse: collapse;">'
#         html += '<tr style="background: #007bff; color: white;">'
#         html += '<th style="padding: 8px;">Subject Code</th>'
#         html += '<th style="padding: 8px;">Subject Name</th>'
#         html += '<th style="padding: 8px;">Units</th>'
#         html += '<th style="padding: 8px;">Instructor</th>'
#         html += '<th style="padding: 8px;">Schedule</th>'
#         html += '</tr>'

#         for i, assignment in enumerate(assignments):
#             schedules = assignment.schedules.all()
#             schedule_info = []
#             for schedule in schedules:
#                 time_range = f"{schedule.time_started.strftime('%I:%M %p')} - {schedule.time_ended.strftime('%I:%M %p')}"
#                 schedule_info.append(f"{schedule.get_frequency_date_display()} {time_range}")

#             schedule_text = "<br>".join(schedule_info) if schedule_info else "No schedule set"
#             bg_color = '#ffffff' if i % 2 == 0 else '#f2f2f2'

#             html += f'<tr style="background: {bg_color};">'
#             html += f'<td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>{assignment.subject.code}</strong></td>'
#             html += f'<td style="padding: 8px; border-bottom: 1px solid #ddd;">{assignment.subject.name}</td>'
#             html += f'<td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">{assignment.subject.unit}</td>'
#             html += f'<td style="padding: 8px; border-bottom: 1px solid #ddd;">{assignment.instructor.name}</td>'
#             html += f'<td style="padding: 8px; border-bottom: 1px solid #ddd;">{schedule_text}</td>'
#             html += '</tr>'

#         html += '</table>'

#         total_units = sum(assignment.subject.unit for assignment in assignments)
#         html += f'<div style="margin-top: 15px; padding-top: 10px; border-top: 2px solid #dee2e6;">'
#         html += f'<p><strong>Total Subjects:</strong> {assignments.count()} | '
#         html += f'<strong>Total Units:</strong> {total_units}</p>'
#         html += '</div>'
#         html += '</div>'

#         return mark_safe(html)
#     subjects_detailed.short_description = 'Subjects & Schedule'


# # ---------- Subject ----------
# @admin.register(Subject)
# class SubjectAdmin(ModelAdmin):
#     list_display = ['code', 'name', 'school', 'unit', 'assignment_count']
#     list_filter = ['school', 'unit']
#     search_fields = ['code', 'name', 'school__school_name']
#     autocomplete_fields = ['school']

#     def assignment_count(self, obj):
#         return obj.assignments.count()
#     assignment_count.short_description = 'Assignments'


# # ---------- Instructor ----------
# @admin.register(Instructor)
# class InstructorAdmin(ModelAdmin):
#     list_display = ['name', 'school', 'display_profile_pic', 'assignment_count', 'sections_taught']
#     list_filter = ['school']
#     search_fields = ['name', 'school__school_name']
#     readonly_fields = ['display_profile_preview', 'teaching_schedule']
#     autocomplete_fields = ['school']

#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('school', 'name', 'profile_picture', 'display_profile_preview')
#         }),
#         ('Teaching Information', {
#             'fields': ('teaching_schedule',),
#             'classes': ('wide',)
#         }),
#     )

#     def display_profile_pic(self, obj):
#         if obj.profile_picture:
#             return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
#         return "No photo"
#     display_profile_pic.short_description = 'Profile'

#     def display_profile_preview(self, obj):
#         if obj.profile_picture:
#             return format_html('<img src="{}" width="200" height="200" style="border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
#         return "No profile picture uploaded"
#     display_profile_preview.short_description = 'Profile Preview'

#     def assignment_count(self, obj):
#         return obj.assignments.count()
#     assignment_count.short_description = 'Assignments'

#     def sections_taught(self, obj):
#         sections = GradeSection.objects.filter(assignments__instructor=obj).distinct()
#         section_list = [str(section) for section in sections[:3]]
#         result = ", ".join(section_list)
#         if sections.count() > 3:
#             result += " ..."
#         return result
#     sections_taught.short_description = 'Sections Teaching'

#     def teaching_schedule(self, obj):
#         assignments = obj.assignments.all()
#         if not assignments:
#             return "No teaching assignments"

#         html = '<table style="width: 100%; border-collapse: collapse;">'
#         html += '<tr style="background: #007bff; color: white;"><th>Section</th><th>Subject</th><th>Schedule</th></tr>'

#         for assignment in assignments:
#             schedules = assignment.schedules.all()
#             schedule_info = []
#             for schedule in schedules:
#                 time_range = f"{schedule.time_started.strftime('%H:%M')}-{schedule.time_ended.strftime('%H:%M')}"
#                 schedule_info.append(f"{schedule.get_frequency_date_display()} {time_range}")
#             schedule_text = ", ".join(schedule_info)

#             html += f'<tr style="border-bottom: 1px solid #ddd;">'
#             html += f'<td>{assignment.grade_section}</td>'
#             html += f'<td>{assignment.subject.name}</td>'
#             html += f'<td>{schedule_text}</td>'
#             html += '</tr>'

#         html += '</table>'
#         return mark_safe(html)
#     teaching_schedule.short_description = 'Teaching Schedule'


# # ---------- Student ----------
# @admin.register(Student)
# class StudentAdmin(ModelAdmin):
#     list_display = [
#         'name', 'school', 'user',
#         'display_profile_pic', 'current_section',
#         'enrollment_history', 'total_units', 'payment_status_summary',
#         'add_payment_link'
#     ]
#     list_filter = ['school', 'user', 'enrollments__grade_section']
#     search_fields = ['name', 'user__username', 'school__school_name']
#     readonly_fields = [
#         'display_profile_preview', 'enrollment_timeline',
#         'current_subjects', 'academic_summary', 'payment_overview'
#     ]
#     autocomplete_fields = ['school', 'user']

#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('school', 'name', 'user', 'profile_picture', 'display_profile_preview')
#         }),
#         ('Enrollment Information', {
#             'fields': ('enrollment_timeline',),
#             'classes': ('wide',)
#         }),
#         ('Academic Information', {
#             'fields': ('current_subjects', 'academic_summary'),
#             'classes': ('wide',)
#         }),
#         ('Payment Information', {
#             'fields': ('payment_overview',),
#             'classes': ('wide',)
#         }),
#     )

#     def display_profile_pic(self, obj):
#         if obj.profile_picture:
#             return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
#         return "No photo"
#     display_profile_pic.short_description = 'Profile'

#     def display_profile_preview(self, obj):
#         if obj.profile_picture:
#             return format_html('<img src="{}" width="200" height="200" style="border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
#         return "No profile picture uploaded"
#     display_profile_preview.short_description = 'Profile Preview'

#     def current_section(self, obj):
#         latest_enrollment = obj.enrollments.order_by('-created_at').first()
#         if latest_enrollment and latest_enrollment.grade_section_id:
#             return format_html(
#                 '<span style="background: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
#                 latest_enrollment.grade_section
#             )
#         return mark_safe('<span style="color: #dc3545;">Not enrolled</span>')
#     current_section.short_description = 'Current Section'

#     def enrollment_history(self, obj):
#         count = obj.enrollments.count()
#         if count == 0:
#             return "Never enrolled"
#         elif count == 1:
#             return "1 enrollment"
#         else:
#             return f"{count} enrollments"
#     enrollment_history.short_description = 'Enrollments'

#     def total_units(self, obj):
#         current_enrollment = obj.enrollments.order_by('-created_at').first()
#         if current_enrollment:
#             assignments = Assignment.objects.filter(grade_section=current_enrollment.grade_section)
#             total = sum(assignment.subject.unit for assignment in assignments)
#             return f"{total} units"
#         return "0 units"
#     total_units.short_description = 'Total Units'

#     def payment_status_summary(self, obj):
#         total_due = Decimal('0')
#         total_paid = Decimal('0')
#         for enrollment in obj.enrollments.all():
#             total_paid += enrollment.payments.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or Decimal('0')
#             total_due += enrollment.payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
#         if total_due == 0:
#             return "No payments"
#         if total_paid >= total_due:
#             return mark_safe('<span style="color: #28a745;">Fully Paid</span>')
#         elif total_paid > 0:
#             percentage = int((total_paid / total_due) * 100)
#             return format_html('<span style="color: #ffc107;">{}% Paid</span>', percentage)
#         else:
#             return mark_safe('<span style="color: #dc3545;">Unpaid</span>')
#     payment_status_summary.short_description = 'Payment Status'

#     def add_payment_link(self, obj):
#         latest_enrollment = obj.enrollments.order_by('-created_at').first()
#         if latest_enrollment:
#             url = reverse('admin:school_payment_add') + f'?enrollment={latest_enrollment.id}'

#             return format_html(
#                 '<a class="px-3 py-1.5 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 transition-colors shadow-sm inline-flex items-center gap-1.5" href="{}">'
#                 '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">'
#                 '<path stroke-linecap="round" stroke-linecap="round" d="M12 4v16m8-8H4"/>'
#                 '</svg>'
#                 '<span>Add Payment</span>'
#                 '</a>',
#                 url
#             )

#         return "—"
#     add_payment_link.short_description = 'Quick Payment'

#     def enrollment_timeline(self, obj):
#         enrollments = obj.enrollments.all().order_by('-created_at')
#         if not enrollments:
#             return "No enrollment history"
#         html = '<div style="max-height: 300px; overflow-y: auto; border: 1px solid #dee2e6; border-radius: 5px;">'
#         html += '<table style="width: 100%; border-collapse: collapse;">'
#         html += '<tr style="background: #28a745; color: white;">'
#         html += '<th style="padding: 10px; text-align: left;">Date Enrolled</th>'
#         html += '<th style="padding: 10px; text-align: left;">Grade Section</th>'
#         html += '<th style="padding: 10px; text-align: left;">Status</th>'
#         html += '</tr>'
#         for i, enrollment in enumerate(enrollments):
#             status = "Current" if i == 0 else "Previous"
#             bg_color = "#28a745" if i == 0 else "#6c757d"
#             row_bg = '#ffffff' if i % 2 == 0 else '#f8f9fa'
#             html += f'<tr style="background: {row_bg};">'
#             html += f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">{enrollment.created_at.strftime("%B %d, %Y at %I:%M %p")}</td>'
#             html += f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;"><strong>{enrollment.grade_section}</strong></td>'
#             html += f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;"><span style="background: {bg_color}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 0.85em;">{status}</span></td>'
#             html += '</tr>'
#         html += '</table></div>'
#         return mark_safe(html)
#     enrollment_timeline.short_description = 'Enrollment Timeline'

#     def current_subjects(self, obj):
#         current_enrollment = obj.enrollments.order_by('-created_at').first()
#         if not current_enrollment:
#             return mark_safe('<div style="color: #dc3545; padding: 20px; text-align: center;">Student is not currently enrolled in any section</div>')
#         grade_section = current_enrollment.grade_section
#         assignments = Assignment.objects.filter(grade_section=grade_section).select_related('subject', 'instructor').prefetch_related('schedules')
#         if not assignments:
#             return mark_safe(f'<div style="color: #856404; background: #fff3cd; padding: 20px; text-align: center; border-radius: 5px;">No subjects assigned to {grade_section}</div>')
#         html = f'<div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">'
#         html += f'<h4 style="margin-top: 0; color: #28a745;">📚 Subjects for {grade_section}</h4>'
#         html += '<table style="width: 100%; border-collapse: collapse; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
#         html += '<thead><tr style="background: #007bff; color: white;">'
#         html += '<th style="padding: 12px; text-align: left;">Code</th>'
#         html += '<th style="padding: 12px; text-align: left;">Subject Name</th>'
#         html += '<th style="padding: 12px; text-align: center;">Units</th>'
#         html += '<th style="padding: 12px; text-align: left;">Instructor</th>'
#         html += '<th style="padding: 12px; text-align: left;">Schedule</th>'
#         html += '</tr></thead><tbody>'
#         for i, assignment in enumerate(assignments):
#             schedules = assignment.schedules.all()
#             schedule_items = []
#             for schedule in schedules:
#                 time_range = f"{schedule.time_started.strftime('%I:%M %p')} - {schedule.time_ended.strftime('%I:%M %p')}"
#                 day_display = schedule.get_frequency_date_display()
#                 schedule_items.append(f'<span style="display: inline-block; background: #e9ecef; padding: 2px 8px; margin: 2px; border-radius: 3px; font-size: 0.9em;">{day_display} {time_range}</span>')
#             schedule_text = '<div>' + ''.join(schedule_items) + '</div>' if schedule_items else '<span style="color: #dc3545;">No schedule set</span>'
#             bg_color = '#ffffff' if i % 2 == 0 else '#f8f9fa'
#             html += f'<tr style="background: {bg_color};">'
#             html += f'<td style="padding: 12px; border-bottom: 1px solid #dee2e6;"><strong>{assignment.subject.code}</strong></td>'
#             html += f'<td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{assignment.subject.name}</td>'
#             html += f'<td style="padding: 12px; border-bottom: 1px solid #dee2e6; text-align: center;"><span style="background: #17a2b8; color: white; padding: 2px 8px; border-radius: 3px;">{assignment.subject.unit}</span></td>'
#             html += f'<td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{assignment.instructor.name}</td>'
#             html += f'<td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{schedule_text}</td>'
#             html += '</tr>'
#         html += '</tbody></table>'
#         total_units = sum(assignment.subject.unit for assignment in assignments)
#         total_subjects = assignments.count()
#         unique_instructors = assignments.values('instructor').distinct().count()
#         html += f'<div style="margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 5px; display: flex; justify-content: space-between; align-items: center;">'
#         html += f'<div><strong>📊 Summary:</strong> {total_subjects} Subject{"s" if total_subjects != 1 else ""}</div>'
#         html += f'<div><strong>📚 Total Units:</strong> <span style="background: #28a745; color: white; padding: 5px 15px; border-radius: 20px;">{total_units}</span></div>'
#         html += f'<div><strong>👨‍🏫 Instructors:</strong> {unique_instructors}</div>'
#         html += '</div></div>'
#         return mark_safe(html)
#     current_subjects.short_description = 'Current Subjects'

#     def academic_summary(self, obj):
#         current_enrollment = obj.enrollments.order_by('-created_at').first()
#         if not current_enrollment:
#             return mark_safe('<div style="color: #6c757d;">No academic data available</div>')
#         grade_section = current_enrollment.grade_section
#         assignments = Assignment.objects.filter(grade_section=grade_section)
#         if not assignments:
#             return mark_safe('<div style="color: #6c757d;">No subjects assigned</div>')
#         total_units = sum(assignment.subject.unit for assignment in assignments)
#         total_subjects = assignments.count()
#         unique_instructors = assignments.values('instructor').distinct().count()
#         all_schedules = Schedule.objects.filter(assignment__in=assignments)
#         day_count = {
#             'MWF': all_schedules.filter(frequency_date='MWF').count(),
#             'TTH': all_schedules.filter(frequency_date='TTH').count(),
#             'EVERYDAY': all_schedules.filter(frequency_date='EVERYDAY').count(),
#         }
#         html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">'
#         html += f'''
#         <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center;">
#             <div style="font-size: 2.5em; font-weight: bold;">{total_subjects}</div>
#             <div style="font-size: 0.9em; opacity: 0.9;">Total Subjects</div>
#         </div>
#         <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 10px; text-align: center;">
#             <div style="font-size: 2.5em; font-weight: bold;">{total_units}</div>
#             <div style="font-size: 0.9em; opacity: 0.9;">Total Units</div>
#         </div>
#         <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 10px; text-align: center;">
#             <div style="font-size: 2.5em; font-weight: bold;">{unique_instructors}</div>
#             <div style="font-size: 0.9em; opacity: 0.9;">Instructors</div>
#         </div>
#         '''
#         html += '</div>'
#         if all_schedules.exists():
#             html += '<div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">'
#             html += '<h5 style="margin-top: 0;">📅 Schedule Distribution</h5>'
#             html += '<div style="display: flex; gap: 10px; flex-wrap: wrap;">'
#             for day, count in day_count.items():
#                 if count > 0:
#                     percentage = (count / all_schedules.count()) * 100
#                     html += f'''
#                     <div style="flex: 1; min-width: 100px; background: white; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
#                         <div style="font-weight: bold;">{day}</div>
#                         <div style="font-size: 0.9em;">{count} class{"es" if count != 1 else ""}</div>
#                         <div style="background: #e9ecef; height: 5px; border-radius: 3px; margin-top: 5px;">
#                             <div style="background: #007bff; width: {percentage}%; height: 5px; border-radius: 3px;"></div>
#                         </div>
#                     </div>
#                     '''
#             html += '</div></div>'
#         return mark_safe(html)
#     academic_summary.short_description = 'Academic Summary'

#     def payment_overview(self, obj):
#         enrollments = obj.enrollments.all()
#         if not enrollments:
#             return "No enrollments"
#         html = ['<div style="max-height: 400px; overflow-y: auto;">']
#         for enrollment in enrollments:
#             payments = enrollment.payments.all()
#             total_due = payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
#             paid = payments.filter(status='PAID').aggregate(paid=Sum('amount'))['paid'] or Decimal('0')
#             assignments = Assignment.objects.filter(grade_section=enrollment.grade_section)
#             total_units = sum(assignment.subject.unit for assignment in assignments)
#             estimated_tuition = Decimal(total_units) * Decimal('360')
#             balance = estimated_tuition - total_due
#             html.append(f'<div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; border-left: 4px solid #007bff;">')
#             html.append(f'<div style="display: flex; justify-content: space-between; align-items: center;">')
#             html.append(f'<h5 style="margin: 0; color: #007bff;">{enrollment.grade_section}</h5>')
#             html.append(f'<small>{enrollment.created_at.strftime("%B %d, %Y")}</small>')
#             html.append('</div>')
#             html.append('<div style="display: flex; gap: 15px; margin: 15px 0;">')
#             html.append(f'<div style="flex: 1; background: white; padding: 10px; border-radius: 5px; text-align: center;">')
#             html.append(f'<div style="font-size: 0.9em; color: #6c757d;">Total Due</div>')
#             html.append(f'<div style="font-size: 1.2em; font-weight: bold;">₱{total_due:,.2f}</div>')
#             html.append('</div>')
#             html.append(f'<div style="flex: 1; background: white; padding: 10px; border-radius: 5px; text-align: center;">')
#             html.append(f'<div style="font-size: 0.9em; color: #6c757d;">Paid</div>')
#             html.append(f'<div style="font-size: 1.2em; font-weight: bold; color: #28a745;">₱{paid:,.2f}</div>')
#             html.append('</div>')
#             html.append(f'<div style="flex: 1; background: white; padding: 10px; border-radius: 5px; text-align: center;">')
#             html.append(f'<div style="font-size: 0.9em; color: #6c757d;">Balance</div>')
#             if balance > 0:
#                 html.append(f'<div style="font-size: 1.2em; font-weight: bold; color: #dc3545;">₱{balance:,.2f}</div>')
#             else:
#                 html.append(f'<div style="font-size: 1.2em; font-weight: bold; color: #28a745;">Fully Paid</div>')
#             html.append('</div>')
#             html.append('</div>')
#             html.append(f'''
#             <div style="margin: 10px 0; padding: 8px; background: #e3f2fd; border-radius: 4px; display: flex; justify-content: space-between;">
#                 <span><strong>Estimated Tuition</strong> (₱360/unit, {total_units} units)</span>
#                 <span style="font-weight: bold; color: #0d47a1;">₱{estimated_tuition:,.2f}</span>
#             </div>
#             ''')
#             if payments.exists():
#                 html.append('<table style="width: 100%; border-collapse: collapse; margin-top: 10px;">')
#                 html.append('<tr style="background: #e9ecef;">')
#                 html.append('<th style="padding: 8px; text-align: left;">Date</th>')
#                 html.append('<th style="padding: 8px; text-align: left;">Amount</th>')
#                 html.append('<th style="padding: 8px; text-align: left;">Method</th>')
#                 html.append('<th style="padding: 8px; text-align: left;">Status</th>')
#                 html.append('<th style="padding: 8px; text-align: left;">Reference</th>')
#                 html.append('</tr>')
#                 for payment in payments.order_by('-payment_date')[:3]:
#                     status_colors = {
#                         'PENDING': '#ffc107',
#                         'PARTIAL': '#17a2b8',
#                         'PAID': '#28a745',
#                         'OVERDUE': '#dc3545',
#                         'CANCELLED': '#6c757d',
#                     }
#                     color = status_colors.get(payment.status, '#6c757d')
#                     status_display = payment.get_status_display()
#                     html.append('<tr style="border-bottom: 1px solid #dee2e6;">')
#                     html.append(f'<td style="padding: 8px;">{payment.payment_date.strftime("%Y-%m-%d")}</td>')
#                     html.append(f'<td style="padding: 8px;">₱{payment.amount:,.2f}</td>')
#                     html.append(f'<td style="padding: 8px;">{payment.get_payment_method_display() or "—"}</td>')
#                     html.append(f'<td style="padding: 8px;"><span style="background: {color}; color: white; padding: 2px 5px; border-radius: 3px; font-size: 0.85em;">{status_display}</span></td>')
#                     html.append(f'<td style="padding: 8px;">{payment.reference_number or "—"}</td>')
#                     html.append('</tr>')
#                 if payments.count() > 3:
#                     html.append(f'<tr><td colspan="5" style="padding: 8px; text-align: center; color: #6c757d;">and {payments.count() - 3} more payments...</td></tr>')
#                 html.append('</table>')
#             else:
#                 html.append('<p style="color: #6c757d; text-align: center; margin: 10px 0;">No payments recorded</p>')
#             html.append('</div>')
#         html.append('</div>')
#         return mark_safe(''.join(html))
#     payment_overview.short_description = 'Payment Overview'

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         if request.user.groups.filter(name='Student').exists():
#             return qs.filter(user=request.user)
#         return qs

#     def has_view_permission(self, request, obj=None):
#         if obj is None:
#             return super().has_view_permission(request, obj)
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='Student').exists():
#             return obj.user == request.user
#         return super().has_view_permission(request, obj)

#     def has_change_permission(self, request, obj=None):
#         if obj is None:
#             return super().has_change_permission(request, obj)
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='Student').exists():
#             return obj.user == request.user
#         return super().has_change_permission(request, obj)

#     def has_delete_permission(self, request, obj=None):
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='Student').exists():
#             return False
#         return super().has_delete_permission(request, obj)

#     def has_add_permission(self, request):
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='Student').exists():
#             return False
#         return super().has_add_permission(request)


# # ---------- Enrollment ----------
# @admin.register(Enrollment)
# class EnrollmentAdmin(ModelAdmin):
#     list_display = ['student', 'grade_section', 'created_at', 'school_name', 'payment_status', 'total_paid', 'payment_count']
#     list_filter = ['grade_section__school', 'grade_section__grade', 'created_at']
#     search_fields = ['student__name', 'grade_section__section_name']
#     date_hierarchy = 'created_at'
#     autocomplete_fields = ['student', 'grade_section']
#     list_select_related = ['student', 'grade_section', 'grade_section__school']
#     inlines = [PaymentInline]
#     readonly_fields = ['payment_summary']

#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('student', 'grade_section', 'created_at')
#         }),
#         ('Payment Information', {
#             'fields': ('payment_summary',),
#             'classes': ('wide',)
#         }),
#     )

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         if request.user.groups.filter(name='Student').exists():
#             return qs.filter(student__user=request.user)
#         return qs

#     def has_view_permission(self, request, obj=None):
#         if obj is None:
#             return super().has_view_permission(request, obj)
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='Student').exists():
#             return obj.student.user == request.user
#         return super().has_view_permission(request, obj)

#     def has_change_permission(self, request, obj=None):
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='Student').exists():
#             return False
#         return super().has_change_permission(request, obj)

#     def has_delete_permission(self, request, obj=None):
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='Student').exists():
#             return False
#         return super().has_delete_permission(request, obj)

#     def has_add_permission(self, request):
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='Student').exists():
#             return False
#         return super().has_add_permission(request)

#     def school_name(self, obj):
#         return obj.grade_section.school.school_name
#     school_name.short_description = 'School'
#     school_name.admin_order_field = 'grade_section__school__school_name'

#     def payment_status(self, obj):
#         payments = obj.payments.all()
#         if not payments:
#             return mark_safe('<span style="color: #dc3545;">No Payments</span>')
#         total = payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
#         paid = payments.filter(status='PAID').aggregate(paid=Sum('amount'))['paid'] or Decimal('0')
#         if paid == 0:
#             return mark_safe('<span style="color: #dc3545;">Unpaid</span>')
#         elif paid < total:
#             percentage = int((paid / total) * 100)
#             return format_html('<span style="color: #ffc107;">{}% Paid</span>', percentage)
#         else:
#             return mark_safe('<span style="color: #28a745;">Fully Paid</span>')
#     payment_status.short_description = 'Payment Status'

#     def total_paid(self, obj):
#         total = obj.payments.filter(status='PAID').aggregate(total=Sum('amount'))['total']
#         total = Decimal(total) if total else Decimal('0')
#         return mark_safe(f'₱{total:,.2f}')
#     total_paid.short_description = 'Total Paid'

#     def payment_count(self, obj):
#         return obj.payments.count()
#     payment_count.short_description = 'Payments'

#     def payment_summary(self, obj):
#         payments = obj.payments.all()
#         if not payments:
#             return mark_safe('<div style="color: #6c757d; padding: 20px; text-align: center;">No payments recorded for this enrollment</div>')
#         total_due = payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
#         paid = payments.filter(status='PAID').aggregate(paid=Sum('amount'))['paid'] or Decimal('0')
#         pending = payments.filter(status='PENDING').aggregate(pending=Sum('amount'))['pending'] or Decimal('0')
#         overdue = payments.filter(status='OVERDUE').aggregate(overdue=Sum('amount'))['overdue'] or Decimal('0')
#         balance = total_due - paid
#         html = ['<div style="background: #f8f9fa; padding: 20px; border-radius: 5px;">']
#         html.append('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">')
#         html.append(f'''
#         <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 5px; text-align: center;">
#             <div style="font-size: 0.9em; opacity: 0.9;">Total Due</div>
#             <div style="font-size: 1.5em; font-weight: bold;">₱{total_due:,.2f}</div>
#         </div>
#         ''')
#         html.append(f'''
#         <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 15px; border-radius: 5px; text-align: center;">
#             <div style="font-size: 0.9em; opacity: 0.9;">Paid</div>
#             <div style="font-size: 1.5em; font-weight: bold;">₱{paid:,.2f}</div>
#         </div>
#         ''')
#         html.append(f'''
#         <div style="background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%); color: white; padding: 15px; border-radius: 5px; text-align: center;">
#             <div style="font-size: 0.9em; opacity: 0.9;">Pending</div>
#             <div style="font-size: 1.5em; font-weight: bold;">₱{pending:,.2f}</div>
#         </div>
#         ''')
#         html.append(f'''
#         <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 15px; border-radius: 5px; text-align: center;">
#             <div style="font-size: 0.9em; opacity: 0.9;">Overdue</div>
#             <div style="font-size: 1.5em; font-weight: bold;">₱{overdue:,.2f}</div>
#         </div>
#         ''')
#         html.append('</div>')
#         if balance > 0:
#             html.append(f'<div style="background: #fff3cd; border: 1px solid #ffeeba; color: #856404; padding: 15px; border-radius: 5px; margin-bottom: 20px; text-align: center;">')
#             html.append(f'<strong>Outstanding Balance: ₱{balance:,.2f}</strong>')
#             html.append('</div>')
#         else:
#             html.append(f'<div style="background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; margin-bottom: 20px; text-align: center;">')
#             html.append('<strong>✓ Fully Paid</strong>')
#             html.append('</div>')
#         html.append('<h5>Payment History</h5>')
#         html.append('<table style="width: 100%; border-collapse: collapse;">')
#         html.append('<tr style="background: #007bff; color: white;">')
#         html.append('<th style="padding: 10px; text-align: left;">Date</th>')
#         html.append('<th style="padding: 10px; text-align: left;">Amount</th>')
#         html.append('<th style="padding: 10px; text-align: left;">Method</th>')
#         html.append('<th style="padding: 10px; text-align: left;">Status</th>')
#         html.append('<th style="padding: 10px; text-align: left;">Reference</th>')
#         html.append('<th style="padding: 10px; text-align: left;">Due Date</th>')
#         html.append('</tr>')
#         status_colors = {
#             'PENDING': '#ffc107',
#             'PARTIAL': '#17a2b8',
#             'PAID': '#28a745',
#             'OVERDUE': '#dc3545',
#             'CANCELLED': '#6c757d',
#         }
#         for payment in payments.order_by('-payment_date'):
#             row_bg = '#ffffff' if list(payments).index(payment) % 2 == 0 else '#f8f9fa'
#             color = status_colors.get(payment.status, '#6c757d')
#             status_display = payment.get_status_display()
#             html.append(f'<tr style="background: {row_bg};">')
#             html.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">{payment.payment_date.strftime("%Y-%m-%d %H:%M")}</td>')
#             html.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">₱{payment.amount:,.2f}</td>')
#             html.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">{payment.get_payment_method_display() or "—"}</td>')
#             html.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;"><span style="background: {color}; color: white; padding: 3px 8px; border-radius: 3px;">{status_display}</span></td>')
#             html.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">{payment.reference_number or "—"}</td>')
#             html.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">{payment.due_date.strftime("%Y-%m-%d") if payment.due_date else "—"}</td>')
#             html.append('</tr>')
#         html.append('</table>')
#         html.append('</div>')
#         return mark_safe(''.join(html))
#     payment_summary.short_description = 'Payment Summary'

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "student" and 'grade_section' in request.GET:
#             try:
#                 grade_section_id = request.GET.get('grade_section')
#                 grade_section = GradeSection.objects.get(id=grade_section_id)
#                 kwargs["queryset"] = Student.objects.filter(school=grade_section.school)
#             except (ValueError, GradeSection.DoesNotExist):
#                 pass
#         elif db_field.name == "grade_section" and 'student' in request.GET:
#             try:
#                 student_id = request.GET.get('student')
#                 student = Student.objects.get(id=student_id)
#                 kwargs["queryset"] = GradeSection.objects.filter(school=student.school)
#             except (ValueError, Student.DoesNotExist):
#                 pass
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


# # ---------- Payment ----------
# @admin.register(Payment)
# class PaymentAdmin(ModelAdmin):
#     list_display = ['enrollment', 'formatted_amount', 'payment_date', 'due_date', 'status_badge', 'payment_method', 'reference_number']
#     list_filter = ['status', 'payment_method', 'payment_date', 'due_date', 'enrollment__grade_section__school']
#     search_fields = ['enrollment__student__name', 'reference_number', 'notes']
#     readonly_fields = ['created_at', 'updated_at', 'is_overdue_display', 'payment_summary']
#     autocomplete_fields = ['enrollment', 'parent_payment']
#     date_hierarchy = 'payment_date'

#     fieldsets = (
#         ('Payment Information', {
#             'fields': ('enrollment', 'amount', 'payment_date', 'due_date', 'status', 'payment_method')
#         }),
#         ('Additional Details', {
#             'fields': ('reference_number', 'notes', 'parent_payment'),
#             'classes': ('wide',)
#         }),
#         ('Payment Status', {
#             'fields': ('is_overdue_display', 'payment_summary'),
#             'classes': ('wide',)
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

#     def formatted_amount(self, obj):
#         amount = Decimal(obj.amount)
#         return mark_safe(f'<span style="font-weight: bold; color: #28a745;">₱{amount:,.2f}</span>')
#     formatted_amount.short_description = 'Amount'
#     formatted_amount.admin_order_field = 'amount'

#     def status_badge(self, obj):
#         colors = {
#             'PENDING': '#ffc107',
#             'PARTIAL': '#17a2b8',
#             'PAID': '#28a745',
#             'OVERDUE': '#dc3545',
#             'CANCELLED': '#6c757d',
#         }
#         color = colors.get(obj.status, '#6c757d')
#         status_display = obj.get_status_display()
#         return format_html(
#             '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
#             color, status_display
#         )
#     status_badge.short_description = 'Status'

#     def is_overdue_display(self, obj):
#         if obj.pk is None:
#             return "Not applicable"
#         if obj.due_date is None:
#             return "No due date set"
#         if obj.is_overdue:
#             return mark_safe('<span style="color: #dc3545; font-weight: bold;">⚠️ OVERDUE</span>')
#         return mark_safe('<span style="color: #28a745;">✓ On Time</span>')
#     is_overdue_display.short_description = 'Overdue Status'

#     def payment_summary(self, obj):
#         if obj.pk is None:
#             return "Payment summary will be available after saving"
#         all_payments = Payment.objects.filter(enrollment=obj.enrollment)
#         total_paid = all_payments.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or Decimal('0')
#         total_pending = all_payments.filter(status='PENDING').aggregate(total=Sum('amount'))['total'] or Decimal('0')
#         installments = obj.installments.all()
#         html = ['<div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">']
#         if installments.exists():
#             html.append('<h5>Installment Payments</h5>')
#             html.append('<table style="width: 100%; border-collapse: collapse;">')
#             html.append('<tr style="background: #007bff; color: white;">')
#             html.append('<th style="padding: 8px;">Amount</th>')
#             html.append('<th style="padding: 8px;">Date</th>')
#             html.append('<th style="padding: 8px;">Status</th>')
#             html.append('<th style="padding: 8px;">Reference</th>')
#             html.append('</tr>')
#             colors = {
#                 'PENDING': '#ffc107',
#                 'PARTIAL': '#17a2b8',
#                 'PAID': '#28a745',
#                 'OVERDUE': '#dc3545',
#                 'CANCELLED': '#6c757d',
#             }
#             for installment in installments:
#                 color = colors.get(installment.status, '#6c757d')
#                 status_display = installment.get_status_display()
#                 html.append('<tr style="border-bottom: 1px solid #dee2e6;">')
#                 html.append(f'<td style="padding: 8px;">₱{installment.amount:,.2f}</td>')
#                 html.append(f'<td style="padding: 8px;">{installment.payment_date.strftime("%Y-%m-%d")}</td>')
#                 html.append(f'<td style="padding: 8px;"><span style="background: {color}; color: white; padding: 2px 5px; border-radius: 3px;">{status_display}</span></td>')
#                 html.append(f'<td style="padding: 8px;">{installment.reference_number or "—"}</td>')
#                 html.append('</tr>')
#             html.append('</table>')
#         html.append(f'''
#         <div style="margin-top: 15px; display: flex; justify-content: space-around; text-align: center;">
#             <div>
#                 <div style="font-size: 1.2em; font-weight: bold; color: #28a745;">₱{total_paid:,.2f}</div>
#                 <div style="font-size: 0.9em; color: #6c757d;">Total Paid</div>
#             </div>
#             <div>
#                 <div style="font-size: 1.2em; font-weight: bold; color: #ffc107;">₱{total_pending:,.2f}</div>
#                 <div style="font-size: 0.9em; color: #6c757d;">Pending</div>
#             </div>
#             <div>
#                 <div style="font-size: 1.2em; font-weight: bold; color: #17a2b8;">{all_payments.count()}</div>
#                 <div style="font-size: 0.9em; color: #6c757d;">Transactions</div>
#             </div>
#         </div>
#         ''')
#         html.append('</div>')
#         return mark_safe(''.join(html))
#     payment_summary.short_description = 'Payment Summary'

#     actions = ['mark_as_paid', 'mark_as_overdue', 'generate_invoice']

#     def mark_as_paid(self, request, queryset):
#         updated = queryset.update(status='PAID')
#         self.message_user(request, f'{updated} payment(s) marked as paid.')
#     mark_as_paid.short_description = "Mark selected payments as PAID"

#     def mark_as_overdue(self, request, queryset):
#         updated = queryset.update(status='OVERDUE')
#         self.message_user(request, f'{updated} payment(s) marked as overdue.')
#     mark_as_overdue.short_description = "Mark selected payments as OVERDUE"

#     def generate_invoice(self, request, queryset):
#         self.message_user(request, 'Invoice generation feature coming soon!')
#     generate_invoice.short_description = "Generate Invoice for selected"


# # ---------- TuitionFee ----------
# @admin.register(TuitionFee)
# class TuitionFeeAdmin(ModelAdmin):
#     list_display = ['school', 'grade', 'fee_type', 'description', 'display_amount', 'is_mandatory', 'school_year']
#     list_filter = ['school', 'grade', 'fee_type', 'is_mandatory', 'school_year']
#     search_fields = ['description', 'school__school_name']
#     list_editable = ['is_mandatory']
#     autocomplete_fields = ['school']

#     def display_amount(self, obj):
#         amount = Decimal(obj.amount)
#         return mark_safe(f'<span style="font-weight: bold;">₱{amount:,.2f}</span>')
#     display_amount.short_description = 'Amount'
#     display_amount.admin_order_field = 'amount'


# # ---------- Assignment ----------
# @admin.register(Assignment)
# class AssignmentAdmin(ModelAdmin):
#     list_display = ['grade_section', 'subject', 'instructor', 'schedule_count', 'school_name']
#     list_filter = ['grade_section__school', 'grade_section__grade', 'subject', 'instructor']
#     search_fields = ['grade_section__section_name', 'subject__name', 'instructor__name']
#     inlines = [ScheduleInline]
#     autocomplete_fields = ['grade_section', 'subject', 'instructor']
#     list_select_related = ['grade_section', 'grade_section__school', 'subject', 'instructor']

#     def school_name(self, obj):
#         return obj.grade_section.school.school_name
#     school_name.short_description = 'School'
#     school_name.admin_order_field = 'grade_section__school__school_name'

#     def schedule_count(self, obj):
#         return obj.schedules.count()
#     schedule_count.short_description = 'Schedules'

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name in ["grade_section", "subject", "instructor"]:
#             school_id = None
#             if 'grade_section' in request.GET:
#                 try:
#                     grade_section = GradeSection.objects.get(id=request.GET['grade_section'])
#                     school_id = grade_section.school_id
#                 except (ValueError, GradeSection.DoesNotExist):
#                     pass
#             if school_id is None and 'subject' in request.GET:
#                 try:
#                     subject = Subject.objects.get(id=request.GET['subject'])
#                     school_id = subject.school_id
#                 except (ValueError, Subject.DoesNotExist):
#                     pass
#             if school_id is None and 'instructor' in request.GET:
#                 try:
#                     instructor = Instructor.objects.get(id=request.GET['instructor'])
#                     school_id = instructor.school_id
#                 except (ValueError, Instructor.DoesNotExist):
#                     pass
#             if school_id:
#                 if db_field.name == "grade_section":
#                     kwargs["queryset"] = GradeSection.objects.filter(school_id=school_id)
#                 elif db_field.name == "subject":
#                     kwargs["queryset"] = Subject.objects.filter(school_id=school_id)
#                 elif db_field.name == "instructor":
#                     kwargs["queryset"] = Instructor.objects.filter(school_id=school_id)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


# # ---------- Schedule ----------
# @admin.register(Schedule)
# class ScheduleAdmin(ModelAdmin):
#     list_display = ['assignment', 'school_name', 'formatted_time', 'frequency_date', 'time_started', 'time_ended']
#     list_filter = ['frequency_date', 'assignment__grade_section__school']
#     search_fields = ['assignment__grade_section__section_name', 'assignment__subject__name']
#     list_editable = ['time_started', 'time_ended', 'frequency_date']
#     autocomplete_fields = ['assignment']
#     list_select_related = ['assignment', 'assignment__grade_section', 'assignment__grade_section__school']

#     def school_name(self, obj):
#         return obj.assignment.grade_section.school.school_name
#     school_name.short_description = 'School'
#     school_name.admin_order_field = 'assignment__grade_section__school__school_name'

#     def formatted_time(self, obj):
#         return f"{obj.time_started.strftime('%I:%M %p')} - {obj.time_ended.strftime('%I:%M %p')}"
#     formatted_time.short_description = 'Time (12hr format)'