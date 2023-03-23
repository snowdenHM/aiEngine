from django.db import models

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    dataset = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name