from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from employer.models import Job
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(blank=False, max_length=150)
    last_name = models.CharField(blank=False, max_length=150)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=50)
    state = models.CharField(blank=True, max_length=10)
    phone = models.CharField(blank=True, max_length=20)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resume_text = models.TextField()
    resume_link = models.TextField()
    similarity=models.DecimalField(null=True,decimal_places=2,max_digits=5)
    personality = models.DecimalField(null=True, decimal_places=2, max_digits=3)
    overall_score=models.DecimalField(null=True,decimal_places=2,max_digits=5)
    def __str__(self):
        return f"Job Application - Job ID: {self.job_id}, User ID: {self.user_id}"
