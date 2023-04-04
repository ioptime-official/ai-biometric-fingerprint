# Generated by Django 3.2.18 on 2023-03-15 11:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0003_rename_user_fileupload_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileupload',
            name='image',
        ),
        migrations.RemoveField(
            model_name='fileupload',
            name='name',
        ),
        migrations.AddField(
            model_name='fileupload',
            name='name_text',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
