from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    requirements = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    personality_1=models.CharField(null=True,max_length=20)
    personality_2 = models.CharField(null=True,max_length=20)
    personality_3 = models.CharField(null=True,max_length=20)

    def __str__(self):
        return self.title
