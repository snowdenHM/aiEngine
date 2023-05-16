from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dataset/', include('dataset.urls', namespace='dataset')),
    path('', include('project.urls', namespace='project')),
    path('__debug__/', include('debug_toolbar.urls'))
]
