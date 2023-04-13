from django.db import models


class Project(models.Model):
    STATUS_CHOICES = (
        ('Complete', 'complete'),
        ('Active', 'active'),
        ('Inactive', 'inactive'),
    )

    project_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name_plural = 'Project'
