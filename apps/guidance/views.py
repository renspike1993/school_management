# exam/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import ExamAttempt, Question
from .services import ExamService


def start_exam(request):
    # attempt = ExamService.start_attempt(request.user)
    # return redirect("exam_page", attempt_id=attempt.id)

    return render(request, "exam/student_exam.html")


def exam_page(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id)

    questions = Question.objects.all().order_by("id")

    # FIX: correct mapping
    existing_answers = {
        ans.question_id: ans.selected_answer
        for ans in attempt.answers.all()
    }

    return render(request, "exam/student_exam.html", {
        "attempt": attempt,
        "questions": questions,
        "existing_answers": existing_answers
    })


def submit_answer(request):
    if request.method == "POST":
        attempt_id = request.POST.get("attempt_id")
        question_id = request.POST.get("question_id")
        answer = request.POST.get("answer")

        attempt = get_object_or_404(ExamAttempt, id=attempt_id)

        ans = ExamService.submit_answer(
            attempt=attempt,
            question_id=question_id,
            selected_answer=answer
        )

        return JsonResponse({
            "status": "ok",
            "correct": ans.is_correct
        })

    return JsonResponse({"status": "error"})


def finish_exam(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id)

    ExamService.finish_attempt(attempt)

    return render(request, "exam/exam_result.html", {
        "attempt": attempt
    })