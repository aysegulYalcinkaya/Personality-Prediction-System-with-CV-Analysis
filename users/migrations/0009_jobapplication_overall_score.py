# Generated by Django 4.2.2 on 2023-08-09 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_jobapplication_personality'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='overall_score',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]