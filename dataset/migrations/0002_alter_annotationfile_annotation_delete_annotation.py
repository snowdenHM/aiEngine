# Generated by Django 4.1.7 on 2023-06-03 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotationfile',
            name='annotation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotationFile', to='dataset.processeddataset'),
        ),
        migrations.DeleteModel(
            name='Annotation',
        ),
    ]