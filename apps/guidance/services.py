# exam/services.py

from django.utils import timezone
from django.db import transaction
from .models import ExamAttempt, Answer, Question, Examinee


class ExamService:

    @staticmethod
    def start_attempt(user):
        examinee, _ = Examinee.objects.get_or_create(user=user)

        return ExamAttempt.objects.create(
            examinee=examinee
        )

    @staticmethod
    def submit_answer(attempt, question_id, selected_answer):
        question = Question.objects.get(id=question_id)

        is_correct = (selected_answer == question.correct_answer)

        answer, _ = Answer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={
                "selected_answer": selected_answer,
                "is_correct": is_correct
            }
        )

        return answer

    @staticmethod
    def finish_attempt(attempt):
        answers = attempt.answers.all()

        total = answers.count()
        correct = answers.filter(is_correct=True).count()

        attempt.score = (correct / total) * 100 if total > 0 else 0
        attempt.finished_at = timezone.now()
        attempt.save()

        return attempt

    @staticmethod
    @transaction.atomic
    def submit_full_exam(user, answers_data):
        examinee, _ = Examinee.objects.get_or_create(user=user)

        attempt = ExamAttempt.objects.create(examinee=examinee)

        for item in answers_data:
            q = Question.objects.get(id=item["question_id"])
            selected = item["answer"]

            Answer.objects.create(
                attempt=attempt,
                question=q,
                selected_answer=selected,
                is_correct=(selected == q.correct_answer)
            )

        ExamService.finish_attempt(attempt)
        return attempt