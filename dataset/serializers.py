from rest_framework import serializers
from dataset.models import File, Folder


class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'
