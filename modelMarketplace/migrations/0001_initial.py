# Generated by Django 4.1.7 on 2023-05-31 11:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataset', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelSetup',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('model_type', models.CharField(blank=True, choices=[('classification', 'Classification'), ('detection', 'Object Detection'), ('segmentation', 'Image Segmentation')], max_length=20, null=True)),
                ('project', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectModel', to='project.project')),
            ],
            options={
                'verbose_name_plural': 'Model Setup',
            },
        ),
        migrations.CreateModel(
            name='ModelTrainingConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('number_of_classes', models.PositiveIntegerField(blank=True, null=True)),
                ('num_of_epochs', models.PositiveIntegerField(blank=True, null=True)),
                ('optimizer', models.CharField(blank=True, choices=[('Adam', 'Adam'), ('SGD', 'SGD'), ('RMSprop', 'RMSprop')], max_length=128, null=True)),
                ('loss', models.CharField(blank=True, choices=[('Mean Absolute Error', 'Mean Absolute Error'), ('Mean Squared Error', 'Mean Squared Error'), ('Root Mean Squared Error', 'Root Mean Squared Error'), ('Binary Cross-Entropy', 'Binary Cross-Entropy'), ('Categorical Cross-Entropy', 'Categorical Cross-Entropy')], max_length=128, null=True)),
                ('fine_tune', models.BooleanField(blank=True, default=False, null=True)),
                ('num_of_layers_unfreeze', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modelTraining', to='modelMarketplace.modelsetup')),
                ('train_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainingSubset', to='dataset.processeddataset')),
                ('val_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validationSubset', to='dataset.processeddataset')),
            ],
            options={
                'verbose_name_plural': 'Model Training Config',
            },
        ),
        migrations.CreateModel(
            name='ModelHistoryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('train_accuracy', models.JSONField(blank=True, null=True)),
                ('val_accuracy', models.JSONField(blank=True, null=True)),
                ('train_loss', models.JSONField(blank=True, null=True)),
                ('val_loss', models.JSONField(blank=True, null=True)),
                ('classification_report', models.JSONField(blank=True, null=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modelHistory', to='modelMarketplace.modelsetup')),
            ],
            options={
                'verbose_name_plural': 'Model History Details',
            },
        ),
    ]
