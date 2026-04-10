from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Examinee,
    QuestionCategory,
    Question,
    ExamAttempt,
    Answer
)


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class QuestionAdmin(ModelAdmin):
    list_display = ("id", "question_type", "category", "short_question")
    list_filter = ("question_type", "category")
    search_fields = ("question_text",)
    ordering = ("-id",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("category", "question_type", "question_text")
        }),

        ("MCQ (Text Choices)", {
            "fields": ("choice_a", "choice_b", "choice_c", "choice_d"),
            "description": "Used only for Multiple Choice Questions"
        }),

        ("Abstract (Image Choices)", {
            "fields": ("image_a", "image_b", "image_c", "image_d"),
            "description": "Used only for Abstract Reasoning Questions"
        }),

        ("Answer", {
            "fields": ("correct_answer",)
        }),
    )

    def short_question(self, obj):
        return (obj.question_text or "Abstract Question")[:40]

    short_question.short_description = "Question"


admin.site.register(Question, QuestionAdmin)


@admin.register(Examinee)
class ExamineeAdmin(ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__email", "user__username")


@admin.register(ExamAttempt)
class ExamAttemptAdmin(ModelAdmin):
    list_display = ("examinee", "started_at", "finished_at", "score")
    list_filter = ("started_at",)


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = ("attempt", "question", "selected_answer", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("question__question_text",)