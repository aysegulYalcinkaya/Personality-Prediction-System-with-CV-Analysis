# Generated by Django 4.2.2 on 2023-08-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_jobapplication_similarity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='similarity',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]