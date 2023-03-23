from django.urls import path
from dataset import views

urlpatterns = [
    # folder
    path('', views.folderView),
    path('<int:pk>', views.folderView),
    path('create', views.folderCreate),
    path('create/<int:parent_id>', views.folderCreate),

    # file
    path('files', views.fileView),
    path('files/<int:pk>', views.fileView),
    path('files/create/<int:folder_id>', views.fileCreate),
]
