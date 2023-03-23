from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from .models import Project
from .serializers import ProjectSerializer


@api_view(['GET'])
def projectView(request, pk=None):

    if request.method == 'GET':
        # Folder Detail View
        if pk is not None:
            try:
                project = Project.objects.get(id=pk)
                data = ProjectSerializer(project).data
            except ObjectDoesNotExist:
                data = {"Error": "Folder does not Exist"}
            return Response(data)

        # Folders List View
        projects = Project.objects.all()
        data = ProjectSerializer(projects, many=True).data
        return Response(data)
    

@api_view(['GET', 'POST'])
def projectCreate(request):

    if request.method == 'POST':
        # Folder Create View
        ser = ProjectSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            project_name = ser.validated_data.get('project_name')
            dataset_name = ser.validated_data.get('dataset_name')
            model_name = ser.validated_data.get('model_name')

            
            project = Project(name=project_name,
                                dataset_name=dataset_name,
                                model_name=model_name)
            project.save()
            return Response(ser.data)
            
               
            

@api_view(['DELETE'])
def projectDelete(request, pid=None):

    
    # ser = ProjectSerializer(data=request.data)
    # if ser.is_valid(raise_exception=True):
    project = Project.objects.get(id=pid)
    project.delete()

    return Response({'message': 'Project deleted successfully'})
    

@api_view(['GET','PUT'])
def projectUpdate(request, pid=None):
    if request.method == 'PUT':
        project = Project.objects.get(id=pid)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)