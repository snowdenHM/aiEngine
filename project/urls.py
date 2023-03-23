from django.urls import path
from dataset import views

urlpatterns = [
    # folder
    path('', views.projectView),
    path('<int:pk>', views.projectView),
    path('delete/<int:pid>', views.projectDelete),
    path('update/<int:pid>', views.projectUpdate),
]