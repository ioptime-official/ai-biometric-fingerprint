# Generated by Django 3.2.18 on 2023-03-16 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0005_fileupload_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='file1/')),
            ],
        ),
    ]
