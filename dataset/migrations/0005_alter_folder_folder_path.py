# Generated by Django 4.1.7 on 2023-03-22 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_alter_folder_folders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='folder_path',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
