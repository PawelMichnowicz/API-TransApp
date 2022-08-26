"""
Serializers for document APIs
"""
from rest_framework import serializers

from document.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    ''' Serializer for document views '''
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['name', 'file_path']

    def get_file_path(self, obj):
        ''' return fiilepath for document object '''
        return obj.file.path


class NipSerializer(serializers.Serializer):
    ''' Serializer handle Nip value '''
    Nip = serializers.CharField(max_length=10)