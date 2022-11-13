from operator import mod
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Role(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role

    class  Meta:
        verbose_name_plural  =  "Roles"

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

    class  Meta:
        verbose_name_plural  =  "Users"

class Document(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=25)
    time_uploaded = models.TimeField(auto_now_add=True)
    date_uploaded = models.DateField(auto_now=True)
    path = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    last_edited = models.DateTimeField(blank=True,null=True)
    class  Meta:
        verbose_name_plural  =  "Documents"

class Student_Document(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)

    class  Meta:
        verbose_name_plural  =  "Students Documents"
