# Generated by Django 3.2.18 on 2023-03-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0004_auto_20230315_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]