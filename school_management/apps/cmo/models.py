from django.db import models
# Create your models here.

# yourapp/choices.py

from django.db import models



class CHEDComplianceCategory(models.TextChoices):
    LEGAL_AUTHORITY = "LEGAL_AUTHORITY", "01 - Legal Authority to Operate"
    PROGRAM_PSGS = "PROGRAM_PSGS", "02 - Program PSGs"
    CURRICULUM_GENERAL_ED = "CURRICULUM_GENERAL_ED", "03 - Curriculum and General Education"
    FACULTY_STAFF = "FACULTY_STAFF", "04 - Faculty and Staff"
    STUDENT_AFFAIRS = "STUDENT_AFFAIRS", "05 - Student Affairs"
    QUALITY_ASSURANCE = "QUALITY_ASSURANCE", "06 - Quality Assurance"
    AUTONOMOUS_DEREGULATED = "AUTONOMOUS_DEREGULATED", "07 - Autonomous / Deregulated"
    RESEARCH_JOURNALS = "RESEARCH_JOURNALS", "08 - Research and Journals"
    COE_COD = "COE_COD", "09 - COE / COD"
    SCHOLARSHIPS_GRANTS = "SCHOLARSHIPS_GRANTS", "10 - Scholarships / Grants"
    HEALTH_SAFETY_FLEXIBLE = "HEALTH_SAFETY_FLEXIBLE", "11 - Health, Safety, Flexible Learning"
    INTERNSHIP_PRACTICUM_CLINICAL = "INTERNSHIP_PRACTICUM_CLINICAL", "12 - Internship / Practicum / Clinical"
    SPORTS_WELLNESS = "SPORTS_WELLNESS", "13 - Sports and Wellness"
    SPECIALIZED_PROGRAMS = "SPECIALIZED_PROGRAMS", "14 - Specialized Programs"
    ETEEAP_LADDERIZED = "ETEEAP_LADDERIZED", "15 - ETEEAP / Ladderized"
    GOVERNANCE_ADMIN = "GOVERNANCE_ADMIN", "16 - Governance / Administration"



class ScopeCategory(models.TextChoices):
    PROGRAM = "LEGAL_AUTHORITY", "01 - Legal Authority to Operate"
    ACADEMICS = "PROGRAM_PSGS", "02 - Program PSGs"






class ChedOrders(models.Model):


    ra_num = models.CharField(max_length=12, blank=True)
    description =  models.CharField(max_length=200, blank=True)
    compliance_category = models.CharField(
        max_length=50,
        choices=CHEDComplianceCategory.choices,
        default=CHEDComplianceCategory.LEGAL_AUTHORITY
    )
    def __str__(self):
        return self.ra_num

    class Meta:
        verbose_name = "Ched Memo Orders"
        verbose_name_plural = " - a.  List of Compliances"
