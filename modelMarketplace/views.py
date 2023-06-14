from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from project.models import Project
from modelMarketplace.models import ModelSetup
from modelMarketplace.forms import ModelSetupForm, ModelTrainingConfigForm
from .utils import train_yolo, prepare_data

def modelCreate(request, pk):
    project = Project.objects.get(id=pk)
    form = ModelSetupForm(request.POST)
    if form.is_valid():
        data = form.save()
    else:
        print(form.errors)

    models = ModelSetup.objects.filter(project=project.id)
    context = {
        "models": models,
        "project": project
    }
    return render(request, 'pages/project/models/modelTable.html', context)

def modelConfig(request, pk):
    if request.method == 'POST':

        project = Project.objects.get(id=pk)
        models = ModelSetup.objects.filter(project=project.id)
        if len(models) == 0:
            form = ModelTrainingConfigForm(request.POST)
            if form.is_valid():
                print("SAVED")
                form.save()
            else:
                print(form.errors)
        else:
            messages.error(request, "Model Config already exists")
            print("Model Config already exists")
    project = Project.objects.get(id=pk)
    models = ModelSetup.objects.filter(project=project.id)
    context = {
        "models": models,
        "project": project
    }
    return render(request, 'pages/project/models/modelTable.html', context)

def modelTraining(request, pk, model_pk):

    project = Project.objects.get(id=pk)
    datasetConfig = project.projectDataset.first()
    modelConfig = project.projectModel.first().modelTraining.first()
 
    result = prepare_data(datasetConfig)
    if result:
        training_result = train_yolo(modelConfig=modelConfig, datasetConfig=datasetConfig)
        messages.success(request, "Training Successful")
    else:
        messages.error(request, "Training Failed")
    return redirect('project:project', pk)


@csrf_exempt
def modelDelete(request, pk, model_pk):
    project = Project.objects.get(id=pk)
    model = ModelSetup.objects.get(id=model_pk)
    model.delete()
    models = ModelSetup.objects.filter(project=project.id)
    context = {
        "models": models,
        "project": project
    }
    return render(request, 'pages/project/models/modelTable.html', context)