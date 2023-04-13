from django.urls import path
from dataset import views

urlpatterns = [
    # folder
    path('folders', views.folderView),
    path('folders/<int:pk>', views.folderView),
    path('folders/create', views.folderCreate),
    path('folders/create/<int:parent_id>', views.folderCreate),

    # file
    path('files', views.fileView),
    path('files/<int:pk>', views.fileView),
    path('files/create/<int:folder_id>', views.fileCreate),
]
