from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from project.models import Project
from project.forms import ProjectForm
from dataset.models import Dataset
from dataset.forms import DatasetForm
from modelMarketplace.models import ModelSetup, ModelTrainingConfig, ModelHistoryDetails
from modelMarketplace.forms import ModelSetupForm, ModelTrainingConfigForm, ModelHistoryDetailsForm

def index(request):
    return render(request, 'dashboard/main.html')


def projectView(request):

    form = ProjectForm()
    data = Project.objects.all()
    context = {"projects": data, "form": form}
    return render(request, 'pages/project/project.html', context)


def projectDetailedView(request, pk):
    project = Project.objects.get(id=pk)
    datasets = Dataset.objects.filter(project=project.id)
    models = ModelSetup.objects.all()
    datasetForm = DatasetForm()
    modelSetupForm = ModelSetupForm()
    modelConfigForm = ModelTrainingConfigForm()
    context = {"project": project,
               "datasets": datasets,
               "datasetForm": datasetForm,
               "models": models,
               "modelForm": modelSetupForm,
               "modelConfigForm": modelConfigForm}
    return render(request, 'pages/project/projectDetail.html', context)


def createProject(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        messages.warning(request, "Unable to add project")
    data = Project.objects.all()
    context = {"projects": data}
    return render(request, 'pages/project/partials/table.html', context)


def projectInstance(request, pk):
    """
    When update button is clicked, this function receives a GET request to render
    Update form populated with the instance associated with the id
    :param request:
    :param pk:
    :return: Update Form with instance
    """
    instance = Project.objects.get(id=pk)
    form = ProjectForm(instance=instance)
    context = {"form": form}
    return render(request, 'pages/project/partials/updateForm.html', context)


def updateProject(request):
    project_id = request.POST.get('id')
    instance = Project.objects.get(id=project_id)
    form = ProjectForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
    else:
        messages.danger(request, "Unable to Update Project")
    data = Project.objects.all()
    context = {"projects": data}
    return render(request, 'pages/project/partials/table.html', context)


@csrf_exempt
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    project.delete()
    data = Project.objects.all()
    context = {"projects": data}
    return render(request, 'pages/project/partials/table.html', context)


