from email.policy import default
from math import e
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models


class ThesisUpload(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    author1 = models.CharField(max_length=200, null=True, blank=True)
    author2 = models.CharField(max_length=200, null=True, blank=True)
    author3 = models.CharField(max_length=200, null=True, blank=True)
    author4 = models.CharField(max_length=200, null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    date_finished = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    file_thesis = models.FileField(upload_to='thesis_files/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    def date_pretty(self):
        return self.date.strftime('%B %Y')