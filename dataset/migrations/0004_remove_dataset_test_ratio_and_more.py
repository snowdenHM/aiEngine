# Generated by Django 4.1.7 on 2023-06-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0003_alter_folder_folder_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='test_ratio',
        ),
        migrations.AlterField(
            model_name='processeddataset',
            name='subset',
            field=models.CharField(blank=True, choices=[('training', 'Training'), ('validation', 'Validation')], max_length=20, null=True),
        ),
    ]
