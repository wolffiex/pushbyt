# Generated by Django 5.0.4 on 2024-04-20 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_animation_main_animat_start_t_db8290_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animation',
            name='file_path',
            field=models.FilePathField(path='render'),
        ),
    ]
