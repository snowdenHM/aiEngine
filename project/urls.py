from django.urls import path
from project import views

app_name = 'project'

urlpatterns = [
    # folder
    # path('api', views.projectView),
    # path('api/<int:pk>', views.projectView),
    # path('api/delete/<int:pid>', views.projectDelete),
    # path('api/update/<int:pid>', views.projectUpdate),

    # views
    path('', views.index, name='index'),
    path('projects', views.projectView, name='projects'),
    path('<int:pk>', views.projectDetailedView, name='project'),
    path('create', views.createProject, name='projectCreate'),
    path('update', views.updateProject, name='projectUpdate'),
    path('instance/<int:pk>', views.projectInstance, name='projectInstance'),
    path('delete/<int:pk>', views.deleteProject, name='projectDelete'),
]
