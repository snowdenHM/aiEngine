# Generated by Django 4.1.7 on 2023-03-22 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0005_alter_folder_folder_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='parents',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parentFolders', to='dataset.folder'),
        ),
    ]