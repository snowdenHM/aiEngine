# Generated by Django 4.1.7 on 2023-06-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0002_alter_annotationfile_annotation_delete_annotation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='folder_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
