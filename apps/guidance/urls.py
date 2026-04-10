# exam/urls.py
from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path("exam/", views.student_exam_page, name="student_exam"),
    path('start/', views.start_exam, name='start_exam'),
    path('exam/<int:attempt_id>/', views.exam_page, name='exam_page'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('finish/<int:attempt_id>/', views.finish_exam, name='finish_exam'),
]