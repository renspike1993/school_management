from django.db import models
from school.models import School
from django.db import models
from school.models import School


class Registrar(models.Model):
    CATEGORY_CHOICES = [
        ('Basic Education', 'Basic Education Institution (BEI\'s)'),
        ('College Education', 'Higher Education Institution (HEI\'s)'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='registrars')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES,default='Basic Education')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school.abbrevation} - {self.category}"

    class Meta:
        verbose_name = "Registrar"
        verbose_name_plural = "- a. List of Members"



class Folder(models.Model):
    registrar = models.ForeignKey(Registrar, on_delete=models.CASCADE, related_name='folders')
    cabinet = models.TextField(blank=True,max_length=255)
    floor = models.TextField(blank=True,max_length=255)
    folder_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.folder_name}"

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "- b. List of Services"
        ordering = ['-created_at']