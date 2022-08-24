from rest_framework import serializers

from document.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['name', 'file_path']

    def get_file_path(self, obj):
        return obj.file.path

