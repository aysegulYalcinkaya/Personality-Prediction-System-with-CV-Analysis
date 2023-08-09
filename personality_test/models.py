from django.db import models
from django.conf import settings

from users.models import CustomUser


class Question(models.Model):
    CATEGORY_CHOICES = (
        ('neuroticism', 'Neuroticism'),
        ('extroversion', 'Extroversion'),
        ('openness', 'Openness'),
        ('agreeableness', 'Agreeableness'),
        ('conscientiousness', 'Conscientiousness'),
    )

    text = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    admin_only = models.BooleanField(default=False)  # New field to indicate if the category is admin-only

    def __str__(self):
        return self.text


class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"

class UserScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    neuroticism = models.DecimalField(decimal_places=2,max_digits=3)
    extroversion = models.DecimalField(decimal_places=2, max_digits=3)
    openness = models.DecimalField(decimal_places=2, max_digits=3)
    agreeableness = models.DecimalField(decimal_places=2, max_digits=3)
    conscientiousness = models.DecimalField(decimal_places=2, max_digits=3)

    def __str__(self):
        return f"{self.user.email} - {self.neuroticism} - {self.extroversion} - {self.openness} - {self.agreeableness} - {self.conscientiousness}"
