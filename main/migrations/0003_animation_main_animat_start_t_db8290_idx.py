# Generated by Django 5.0.4 on 2024-04-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_deadline_animation_start_time'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='animation',
            index=models.Index(fields=['start_time'], name='main_animat_start_t_db8290_idx'),
        ),
    ]