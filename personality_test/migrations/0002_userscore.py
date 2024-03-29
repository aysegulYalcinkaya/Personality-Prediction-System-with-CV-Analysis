# Generated by Django 4.2.2 on 2023-08-09 02:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personality_test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('neuroticism', models.DecimalField(decimal_places=2, max_digits=2)),
                ('extroversion', models.DecimalField(decimal_places=2, max_digits=2)),
                ('openness', models.DecimalField(decimal_places=2, max_digits=2)),
                ('agreeableness', models.DecimalField(decimal_places=2, max_digits=2)),
                ('conscientiousness', models.DecimalField(decimal_places=2, max_digits=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
