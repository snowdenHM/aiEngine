from django.urls import path
from modelMarketplace import views

app_name = 'model'

urlpatterns = [
    path('<int:pk>/create', views.modelCreate, name='modelCreate'),
    path('<int:pk>/createConfig', views.modelConfig, name='modelConfig'),
    path('<int:pk>/delete/<str:model_pk>', views.modelDelete, name='modelDelete'),
    path('<int:pk>/training/<str:model_pk>', views.modelTraining, name='modelTraining'),
]
