from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Examinee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    class Meta:
        verbose_name = "Examinee"
        verbose_name_plural = "_1.1 Examinees"
    
    
    
class QuestionCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "_1.2 Exam Categories"


class Question(models.Model):

    QUESTION_TYPES = (
        ('mcq', 'Text Type'),
        ('abstract', 'Image Type'),
    )

    category = models.ForeignKey(
        'QuestionCategory',
        on_delete=models.CASCADE,
        related_name="questions",
        null=True,
        blank=True
    )

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default='mcq'
    )

    question_text = models.TextField(blank=True, null=True)

    # =========================
    # MCQ (text-based)
    # =========================
    choice_a = models.CharField(max_length=255, blank=True, null=True)
    choice_b = models.CharField(max_length=255, blank=True, null=True)
    choice_c = models.CharField(max_length=255, blank=True, null=True)
    choice_d = models.CharField(max_length=255, blank=True, null=True)

    # =========================
    # ABSTRACT (image-based)
    # =========================
    image_a = models.ImageField(upload_to='abstract_choices/', blank=True, null=True)
    image_b = models.ImageField(upload_to='abstract_choices/', blank=True, null=True)
    image_c = models.ImageField(upload_to='abstract_choices/', blank=True, null=True)
    image_d = models.ImageField(upload_to='abstract_choices/', blank=True, null=True)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ],
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "_1.3 Questions"

    def __str__(self):
        return (self.question_text or "Abstract Question")[:50]
    
    
class ExamAttempt(models.Model):
    examinee = models.ForeignKey(
        Examinee,
        on_delete=models.CASCADE,
        related_name="attempts"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    score = models.FloatField(default=0)


    class Meta:
        verbose_name = "Attempt"
        verbose_name_plural = "_1.4 Exam Attempts"

    def __str__(self):
        return f"{self.examinee} - Attempt {self.id}"


class Answer(models.Model):
    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    selected_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ],
        blank=True,
        null=True
    )

    is_correct = models.BooleanField(default=False)

    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("attempt", "question")
        verbose_name = "Answer"
        verbose_name_plural = "_1.5 Answers"
        
        
    def __str__(self):
        return f"{self.attempt} - {self.question}"