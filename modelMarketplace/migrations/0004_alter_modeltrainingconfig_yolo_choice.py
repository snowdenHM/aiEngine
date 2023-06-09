# Generated by Django 4.1.7 on 2023-06-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelMarketplace', '0003_remove_modeltrainingconfig_fine_tune_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modeltrainingconfig',
            name='yolo_choice',
            field=models.CharField(blank=True, choices=[('yolov5n', 'YOLOv5 Nano'), ('yolov5s', 'YOLOv5 Small'), ('yolov5m', 'YOLOv5 Medium'), ('yolov5l', 'YOLOv5 Large'), ('yolov5x', 'YOLOv5 Extra-Large')], default='yolov5s', max_length=50, null=True),
        ),
    ]
