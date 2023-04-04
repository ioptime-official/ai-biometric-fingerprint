
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
# this is for the registration of user
class FileUpload(models.Model):
    name_text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.name_text
# this is for matching user
class UploadMatch(models.Model):
    image = models.ImageField(upload_to='file1/', null=True, blank=True)
    def __str__(self):
        return self.image
