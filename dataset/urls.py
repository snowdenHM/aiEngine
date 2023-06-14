from django.urls import path
from dataset import views

app_name = 'dataset'

urlpatterns = [
    path('<int:pk>/create', views.datasetCreate, name='datasetCreate'),
    path('<int:pk>/delete/<str:data_pk>', views.datasetDelete, name='datasetDelete'),
    path('<int:pk>/getData', views.getStorageData, name='s3Data'),
]
