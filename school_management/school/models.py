from django.db import models


class ChedOrders(models.Model):
    ra_num = models.CharField(max_length=12, blank=True)
    
    
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
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='programs'
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
        return f" { self.abbreviation } - { self.major }" or self.program_name or "Unnamed Program"

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "- b. List of Programs"


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
        return self.program.program_name

    class Meta:
        verbose_name = "Curriculum"
        verbose_name_plural = "- c. List of Curriculums"
        
        
class Subject(models.Model):
    
    subject_code = models.CharField(max_length=100, blank=True)
    subject_desc = models.CharField(max_length=100, blank=True)
    subject_unit = models.IntegerField(default=2,blank=False)
    GROUP_CHOICES = [
        ('I', 'I - Major Subject'),
        ('II', 'II - Elective Subject'),
        ('III', 'III - Minor Subject'),
        ('IV', 'IV - Other'),
        ('V', 'V - Institutional Subject'),
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
        
        


class Books(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='books',
        blank=True,
        null=True  # <-- allow null for now
    )
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.subject.subject_code

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "- e. List of Books Holdings"
        
        

