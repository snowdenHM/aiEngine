from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from dataset.models import Folder, File
from dataset.serializers import FolderSerializer, FileSerializer
from django.shortcuts import render, redirect


####################### FILE STRUCTURE API VIEWS ###########################
@api_view(['GET'])
def folderView(request, pk=None):

    if request.method == 'GET':
        # Folder Detail View
        if pk is not None:
            try:
                folder = Folder.objects.get(id=pk)
                data = FolderSerializer(folder).data
            except ObjectDoesNotExist:
                data = {"Error": "Folder does not Exist"}
            return Response(data)

        # Folders List View
        folders = Folder.objects.all()
        data = FolderSerializer(folders, many=True).data
        return Response(data)


@api_view(['GET', 'POST'])
def folderCreate(request, parent_id=None):

    if request.method == 'POST':
        # Folder Create View
        ser = FolderSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            folder_name = ser.validated_data.get('name')

            if parent_id is not None:
                parent_folder = Folder.objects.get(id=parent_id)
                folder_path = parent_folder.folder_path + "/" + folder_name
                folder = Folder(folder_name=folder_name,
                                folder_path=folder_path,
                                parents=parent_folder)
                folder.save()
                parent_folder.folders.add(folder.id)
            else:
                folder = Folder(folder_name=folder_name,
                                folder_path=folder_name,
                                parents=None)
                folder.save()
            return Response(ser.data)


@api_view(['GET'])
def fileView(request, pk=None):

    if request.method == 'GET':
        # File Detail View
        if pk is not None:
            try:
                file = File.objects.get(id=pk)
                data = FileSerializer(file).data
            except ObjectDoesNotExist:
                data = {"Error": "Folder does not Exist"}
            return Response(data)

        # Files List View
        files = File.objects.all()
        data = FileSerializer(files, many=True).data
        return Response(data)


@api_view(['GET', 'POST'])
def fileCreate(request, folder_id=None):

    if request.method == 'POST':
        # File Create View
        ser = FileSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):

            folder = Folder.objects.get(id=folder_id)
            doc = ser.validated_data['file_upload']
            fileName = doc.name
            fileExt = doc.name.split('.')[-1]
            fileSize = doc.size
            filePath = folder.folder_path + "/" + fileName

            file = File(file_name=fileName,
                        file_path=filePath,
                        file_size=fileSize,
                        file_extension=fileExt,
                        file_upload=doc,
                        parent=folder)
            file.save()

            return Response(ser.data)

##################### RENDER VIEWS ######################



