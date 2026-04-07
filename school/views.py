# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
# from django.db.models import Sum
# from decimal import Decimal
# from .models import Student, Assignment, Schedule

# @login_required
# def student_profile(request):
#     # Try to find the student whose name matches the logged‑in user's username.
#     # This assumes each student's username is exactly their full name (unique).
#     try:
#         student = Student.objects.get(name=request.user.username)
#     except Student.DoesNotExist:
#         # If no match, show a friendly error message.
#         return render(request, 'error.html', {
#             'message': 'No student profile is linked to your account. Please contact the administrator.'
#         })

#     # Gather all enrollments for this student (newest first)
#     enrollments = student.enrollments.all().order_by('-created_at')

#     # Build a list of enrollment data for the template
#     enrollment_data = []
#     for enrollment in enrollments:
#         grade_section = enrollment.grade_section
#         payments = enrollment.payments.all()
#         total_due = payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
#         paid = payments.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or Decimal('0')

#         # Subjects & assignments for this grade section
#         assignments = Assignment.objects.filter(grade_section=grade_section)\
#                          .select_related('subject', 'instructor')\
#                          .prefetch_related('schedules')
#         subjects = []
#         total_units = 0
#         for assignment in assignments:
#             total_units += assignment.subject.unit
#             schedules = assignment.schedules.all()
#             schedule_list = []
#             for schedule in schedules:
#                 time_range = f"{schedule.time_started.strftime('%I:%M %p')} - {schedule.time_ended.strftime('%I:%M %p')}"
#                 schedule_list.append(f"{schedule.get_frequency_date_display()} {time_range}")
#             subjects.append({
#                 'code': assignment.subject.code,
#                 'name': assignment.subject.name,
#                 'units': assignment.subject.unit,
#                 'instructor': assignment.instructor.name,
#                 'schedules': schedule_list,
#             })

#         # Payment history (last 3 payments)
#         payment_history = payments.order_by('-payment_date')[:3]

#         enrollment_data.append({
#             'enrollment': enrollment,
#             'grade_section': grade_section,
#             'total_due': total_due,
#             'paid': paid,
#             'balance': total_due - paid,
#             'subjects': subjects,
#             'total_units': total_units,
#             'estimated_tuition': Decimal(total_units) * Decimal('360'),
#             'payment_history': payment_history,
#         })

#     context = {
#         'student': student,
#         'enrollment_data': enrollment_data,
#     }
#     return render(request, 'student_profile.html', context)


# @login_required
# def post_login_redirect(request):
#     """
#     Redirect users after login based on their group/staff status.
#     Staff → admin dashboard, Students → student profile, fallback → profile.
#     """
#     user = request.user
#     if user.is_staff or user.is_superuser:
#         return redirect('admin:index')
#     if user.groups.filter(name='Student').exists():
#         return redirect('student_profile')
#     # Fallback (should not normally happen)
#     return redirect('student_profile')




def home(request):

    return render(request,"base.html")