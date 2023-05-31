from rest_framework import serializers
from .models import FileUpload
from .models import UploadMatch

class FingerprintSerializer(serializers.ModelSerializer):
	class Meta:
		model = FileUpload
		fields = ['name_text', 'image']

class MatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = UploadMatch
		fields = ['image']



