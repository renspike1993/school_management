from django.db import models

from apps.cmo.models import ChedOrders
    
class School(models.Model):
    abbrevation = models.CharField(max_length=12, blank=True,verbose_name="School Abbr")
    school_name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=500, blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    started_at = models.DateField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    def __str__(self):
        return self.school_name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = " - a.  List of HEI's"


class Program(models.Model):
    
    ched_orders = models.ForeignKey(
        ChedOrders,
        on_delete=models.CASCADE,
        related_name='ched_orders',
        blank=True,
        null=True  # <-- allow null for now
    )
    program_name = models.CharField(max_length=100, blank=True)
    abbreviation = models.CharField(max_length=12, blank=True)
    major = models.CharField(max_length=12, blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Program Status"
    )
    started_at = models.DateField()

    def __str__(self):
        return f" { self.abbreviation } - { self.major }" or { } or "Unnamed Program"

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "- b. List of Programs"


        
        
class Subject(models.Model):
    
    subject_code = models.CharField(max_length=100, blank=True)
    subject_desc = models.CharField(max_length=100, blank=True)
    subject_unit = models.IntegerField(default=2,blank=False)
    GROUP_CHOICES = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
        ('VI', 'VI'),
        ('VII', 'VII'),
        ('VIII', 'VIII'),
        ('IX', 'IX'),
        ('X', 'X'),

    ]
    unit_group = models.CharField(
        max_length=10,
        choices=GROUP_CHOICES,
        default='V',
        verbose_name="Unit Group"
    )
    def __str__(self):
        return f"{self.subject_code}-{self.subject_desc}"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "- d. List of Subjects"
        
        

class Curriculum(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name='curriculums',
        blank=True,
        null=True  # <-- allow null for now
    )
    
    curriculum_name = models.CharField(max_length=100, blank=True)
    started_at = models.DateField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approved Status"
    )
    def __str__(self):
        return f"{self.program}"

    class Meta:
        verbose_name = "Curriculum"
        verbose_name_plural = "- c. List of Curriculums"

class Books(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='books',
        blank=True,
        null=True  # <-- allow null for now
    )
    title = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    COLLECTION_CHOICES = [
        ('Circulation', 'Circulation'),
        ('Filipiniana', 'Filipiniana'),
        ('References', 'References'),
        ('General', 'General'),

    ]
    collection = models.CharField(
        max_length=20,
        choices=COLLECTION_CHOICES,
        default='General',
        verbose_name="Collections"
    )

    def __str__(self):
        return self.subject.subject_code

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "- e. List of Books"
        
        


class Syllabus(models.Model):
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='subject_curriculum',
        blank=True,
        null=True  # <-- allow null for now
    )
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        related_name='syllabus_curriculum',
        blank=True,
        null=True  # <-- allow null for now
    )
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Syllabus Status"
    )

    def __str__(self):
        return f"{self.subject} if {self.subject} else {'No Related Record'}"

    class Meta:
        verbose_name = "Syllaby"
        verbose_name_plural = "- f.  List of Syllabus"

